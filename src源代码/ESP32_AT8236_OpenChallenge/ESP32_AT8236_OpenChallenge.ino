/*
 * 2026 WRO Future Engineers - ESP32 + AT8236 hardware baseline
 * This diagnostic sketch disables Wi-Fi and Bluetooth for rule compliance.
 * It intentionally runs at low PWM and requires a physical start button.
 */
#include <WiFi.h>
#include <esp_bt.h>
#include <ESP32Servo.h>

const byte PIN_SERVO = 32;
const byte PIN_MOTOR_A = 27;
const byte PIN_MOTOR_B = 12;
const byte PIN_ENCODER_A = 14;
const byte PIN_ENCODER_B = 13;
const byte PIN_FRONT_TRIG = 25;
const byte PIN_FRONT_ECHO = 26;
const byte PIN_RIGHT_TRIG = 18;
const byte PIN_RIGHT_ECHO = 19;
const byte PIN_START = 33;

const int SERVO_RIGHT = 55, SERVO_CENTER = 90, SERVO_LEFT = 115;
const int TEST_PWM = 80;
const float STOP_DISTANCE_CM = 18.0f;
volatile long encoderTicks = 0;
bool running = false;
Servo steering;

void IRAM_ATTR encoderISR() {
  encoderTicks += (digitalRead(PIN_ENCODER_A) == digitalRead(PIN_ENCODER_B)) ? 1 : -1;
}

float distanceCm(byte trig, byte echo) {
  digitalWrite(trig, LOW); delayMicroseconds(2);
  digitalWrite(trig, HIGH); delayMicroseconds(10); digitalWrite(trig, LOW);
  unsigned long us = pulseIn(echo, HIGH, 25000);
  return us == 0 ? 999.0f : us * 0.0343f * 0.5f;
}

void motor(int pwm) {
  pwm = constrain(pwm, -120, 120);
  if (pwm > 0) { analogWrite(PIN_MOTOR_A, pwm); digitalWrite(PIN_MOTOR_B, LOW); }
  else if (pwm < 0) { digitalWrite(PIN_MOTOR_A, LOW); analogWrite(PIN_MOTOR_B, -pwm); }
  else { digitalWrite(PIN_MOTOR_A, HIGH); digitalWrite(PIN_MOTOR_B, HIGH); }
}

void setup() {
  // WRO rules prohibit wireless communication during the match.
  WiFi.mode(WIFI_OFF);
  WiFi.disconnect(true);
  btStop();

  Serial.begin(115200);
  pinMode(PIN_MOTOR_A, OUTPUT); pinMode(PIN_MOTOR_B, OUTPUT);
  pinMode(PIN_ENCODER_A, INPUT_PULLUP); pinMode(PIN_ENCODER_B, INPUT_PULLUP);
  pinMode(PIN_FRONT_TRIG, OUTPUT); pinMode(PIN_FRONT_ECHO, INPUT);
  pinMode(PIN_RIGHT_TRIG, OUTPUT); pinMode(PIN_RIGHT_ECHO, INPUT);
  pinMode(PIN_START, INPUT_PULLUP);
  ESP32PWM::allocateTimer(1); ESP32PWM::allocateTimer(2); ESP32PWM::allocateTimer(3);
  steering.setPeriodHertz(50); steering.attach(PIN_SERVO, 500, 2500);
  steering.write(SERVO_CENTER); motor(0);
  attachInterrupt(digitalPinToInterrupt(PIN_ENCODER_A), encoderISR, RISING);
  Serial.println("ESP32 baseline ready; wireless disabled; press start.");
}

void loop() {
  static bool oldButton = HIGH;
  bool button = digitalRead(PIN_START);
  if (oldButton == HIGH && button == LOW) { running = !running; delay(30); }
  oldButton = button;

  float front = distanceCm(PIN_FRONT_TRIG, PIN_FRONT_ECHO);
  delayMicroseconds(1500);
  float right = distanceCm(PIN_RIGHT_TRIG, PIN_RIGHT_ECHO);
  if (front < STOP_DISTANCE_CM) running = false;

  if (running) {
    int steerCommand = right >= 900.0f ? 0 : constrain((int)((right - 30.0f) * 1.8f), -70, 70);
    int servoAngle = steerCommand < 0
      ? map(steerCommand, -100, 0, SERVO_LEFT, SERVO_CENTER)
      : map(steerCommand, 0, 100, SERVO_CENTER, SERVO_RIGHT);
    steering.write(servoAngle); motor(TEST_PWM);
  } else { steering.write(SERVO_CENTER); motor(0); }

  noInterrupts(); long ticks = encoderTicks; encoderTicks = 0; interrupts();
  Serial.printf("run=%d,front=%.1f,right=%.1f,ticks=%ld\n", running, front, right, ticks);
  delay(50);
}
