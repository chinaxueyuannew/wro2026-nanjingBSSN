/*
 * 2026 WRO Future Engineers - Open Challenge baseline
 * Hardware: Arduino UNO + AT8236 + four-wheel-drive Ackermann chassis (previous experiment)
 *
 * Functions:
 * - independent start button; the vehicle remains stopped after power-on
 * - Hall encoder speed PI control
 * - right-wall PD steering
 * - front-corner state machine and emergency stop
 * - serial telemetry for reproducible tuning
 *
 * IMPORTANT: verify every pin and physical constant on the actual vehicle.
 */
#include <Servo.h>

// ---------- Pin assignment: AT8236 uses two PWM inputs ----------
const byte PIN_ENCODER_A = 2;  // yellow, interrupt pin
const byte PIN_ENCODER_B = 4;  // white
const byte PIN_MOTOR_A = 5;
const byte PIN_MOTOR_B = 6;
const byte PIN_US_FRONT_TRIG = 7;
const byte PIN_US_FRONT_ECHO = 8;
const byte PIN_SERVO = 9;
const byte PIN_US_RIGHT_TRIG = 10;
const byte PIN_US_RIGHT_ECHO = 11;
const byte PIN_START = 12;     // button to GND, INPUT_PULLUP
const byte PIN_LED = 13;

// ---------- Chassis specification parameters; verify on the team vehicle ----------
const float ENCODER_CPR = 12.0f;
const float GEAR_RATIO = 8.864f;
const float WHEEL_DIAMETER_M = 0.047f;

// Servo calibration. The team's early test range is about 55..115 degrees.
const int SERVO_RIGHT = 55;
const int SERVO_CENTER = 90;
const int SERVO_LEFT = 115;

// ---------- Control parameters: tune from tests ----------
const float TARGET_SPEED_MPS = 0.35f;
const float SPEED_KP = 260.0f;
const float SPEED_KI = 110.0f;
const int PWM_MIN_MOVING = 45;
const int PWM_LIMIT = 150;       // conservative first-test limit

const float TARGET_RIGHT_CM = 30.0f;
const float WALL_KP = 1.8f;
const float WALL_KD = 3.0f;
const int MAX_STEER_COMMAND = 80;

const float FRONT_EMERGENCY_CM = 14.0f;
const float FRONT_TURN_CM = 38.0f;
const unsigned long TURN_TIME_MS = 720;
const unsigned long SENSOR_TIMEOUT_US = 25000;
const unsigned long CONTROL_PERIOD_MS = 50;

enum RobotState { WAIT_START, FOLLOW_WALL, TURN_LEFT, EMERGENCY_STOP };
RobotState state = WAIT_START;
Servo steering;
volatile long encoderTicks = 0;

float measuredSpeed = 0.0f;
float speedIntegral = 0.0f;
float previousWallError = 0.0f;
float filteredFront = 999.0f;
float filteredRight = 999.0f;
unsigned long lastControlMs = 0;
unsigned long stateStartMs = 0;

void encoderISR() {
  encoderTicks += (digitalRead(PIN_ENCODER_B) == LOW) ? 1 : -1;
}

float readDistanceCm(byte trig, byte echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  unsigned long duration = pulseIn(echo, HIGH, SENSOR_TIMEOUT_US);
  if (duration == 0) return 999.0f;
  float cm = duration * 0.0343f * 0.5f;
  if (cm < 2.0f || cm > 300.0f) return 999.0f;
  return cm;
}

float lowPass(float previous, float sample) {
  if (sample >= 900.0f) return sample;
  if (previous >= 900.0f) return sample;
  return 0.65f * previous + 0.35f * sample;
}

void setMotorPwm(int pwm) {
  pwm = constrain(pwm, -PWM_LIMIT, PWM_LIMIT);
  if (pwm > 0) {
    analogWrite(PIN_MOTOR_A, pwm);
    digitalWrite(PIN_MOTOR_B, LOW);
  } else if (pwm < 0) {
    digitalWrite(PIN_MOTOR_A, LOW);
    analogWrite(PIN_MOTOR_B, -pwm);
  } else {
    // The team's AT8236 experiment uses both HIGH as braking/stop.
    digitalWrite(PIN_MOTOR_A, HIGH);
    digitalWrite(PIN_MOTOR_B, HIGH);
  }
}

void setSteering(int command) {
  command = constrain(command, -100, 100);
  int angle;
  if (command < 0) {
    angle = map(command, -100, 0, SERVO_LEFT, SERVO_CENTER);
  } else {
    angle = map(command, 0, 100, SERVO_CENTER, SERVO_RIGHT);
  }
  steering.write(constrain(angle, SERVO_RIGHT, SERVO_LEFT));
}

void stopSafely() {
  setMotorPwm(0);
  setSteering(0);
  speedIntegral = 0.0f;
}

bool startButtonPressed() {
  static bool stable = HIGH;
  static bool rawPrevious = HIGH;
  static unsigned long changedAt = 0;
  bool raw = digitalRead(PIN_START);
  if (raw != rawPrevious) {
    changedAt = millis();
    rawPrevious = raw;
  }
  if (millis() - changedAt > 25 && raw != stable) {
    stable = raw;
    return stable == LOW;
  }
  return false;
}

void updateMeasuredSpeed(float dt) {
  noInterrupts();
  long ticks = encoderTicks;
  encoderTicks = 0;
  interrupts();
  float revolutions = ticks / (ENCODER_CPR * GEAR_RATIO);
  measuredSpeed = fabs(revolutions * PI * WHEEL_DIAMETER_M / dt);
}

int speedController(float target, float dt) {
  float error = target - measuredSpeed;
  speedIntegral += error * dt;
  speedIntegral = constrain(speedIntegral, -0.7f, 0.7f);
  int pwm = (int)(SPEED_KP * error + SPEED_KI * speedIntegral);
  if (target > 0.01f && pwm > 0 && pwm < PWM_MIN_MOVING) pwm = PWM_MIN_MOVING;
  return constrain(pwm, 0, PWM_LIMIT);
}

int wallController(float rightCm, float dt) {
  if (rightCm >= 900.0f) {
    previousWallError = 0.0f;
    return 0;  // degraded mode: straight until a valid reading returns
  }
  float error = rightCm - TARGET_RIGHT_CM;
  float derivative = (error - previousWallError) / dt;
  previousWallError = error;
  int command = (int)(WALL_KP * error + WALL_KD * derivative);
  return constrain(command, -MAX_STEER_COMMAND, MAX_STEER_COMMAND);
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_ENCODER_A, INPUT_PULLUP);
  pinMode(PIN_ENCODER_B, INPUT_PULLUP);
  pinMode(PIN_MOTOR_A, OUTPUT);
  pinMode(PIN_MOTOR_B, OUTPUT);
  pinMode(PIN_US_FRONT_TRIG, OUTPUT);
  pinMode(PIN_US_FRONT_ECHO, INPUT);
  pinMode(PIN_US_RIGHT_TRIG, OUTPUT);
  pinMode(PIN_US_RIGHT_ECHO, INPUT);
  pinMode(PIN_START, INPUT_PULLUP);
  pinMode(PIN_LED, OUTPUT);
  steering.attach(PIN_SERVO);
  attachInterrupt(digitalPinToInterrupt(PIN_ENCODER_A), encoderISR, RISING);
  stopSafely();
  lastControlMs = millis();
  Serial.println(F("WRO UNO+AT8236 ready; press the start button."));
}

void loop() {
  if (startButtonPressed()) {
    if (state == WAIT_START || state == EMERGENCY_STOP) {
      state = FOLLOW_WALL;
      stateStartMs = millis();
      speedIntegral = 0.0f;
    } else {
      state = EMERGENCY_STOP;  // same button can stop during testing
    }
  }

  unsigned long now = millis();
  if (now - lastControlMs < CONTROL_PERIOD_MS) return;
  float dt = (now - lastControlMs) / 1000.0f;
  lastControlMs = now;

  updateMeasuredSpeed(dt);
  filteredFront = lowPass(filteredFront, readDistanceCm(PIN_US_FRONT_TRIG, PIN_US_FRONT_ECHO));
  delayMicroseconds(1500); // reduce ultrasonic cross-talk
  filteredRight = lowPass(filteredRight, readDistanceCm(PIN_US_RIGHT_TRIG, PIN_US_RIGHT_ECHO));

  if (state != WAIT_START && filteredFront < FRONT_EMERGENCY_CM) {
    state = EMERGENCY_STOP;
  }

  switch (state) {
    case WAIT_START:
      stopSafely();
      break;
    case FOLLOW_WALL:
      if (filteredFront < FRONT_TURN_CM) {
        state = TURN_LEFT;
        stateStartMs = now;
      } else {
        setSteering(wallController(filteredRight, dt));
        setMotorPwm(speedController(TARGET_SPEED_MPS, dt));
      }
      break;
    case TURN_LEFT:
      setSteering(-85);
      setMotorPwm(speedController(TARGET_SPEED_MPS * 0.70f, dt));
      if (now - stateStartMs >= TURN_TIME_MS && filteredFront > FRONT_TURN_CM + 8.0f) {
        state = FOLLOW_WALL;
        previousWallError = 0.0f;
      }
      break;
    case EMERGENCY_STOP:
      stopSafely();
      break;
  }

  digitalWrite(PIN_LED, state == FOLLOW_WALL || state == TURN_LEFT);
  Serial.print((int)state); Serial.print(',');
  Serial.print(filteredFront, 1); Serial.print(',');
  Serial.print(filteredRight, 1); Serial.print(',');
  Serial.println(measuredSpeed, 3);
}
