/*
 * 2026 WRO Future Engineers - Vision Serial Executor
 * 2026 WRO未来工程师——视觉串口执行端
 *
 * Team / 队伍: BONA SONORITY SCHOOL NANJING / 南京博颂学校
 * Target / 目标: Arduino UNO + PWM/DIR motor-driver interface
 *
 * This program is the competition-candidate lower-level controller for the
 * current vision-only architecture. It accepts ASCII lines from the Orange Pi:
 *
 *   steer,speed\n
 *
 * Both values must be integers in -100..100. The vehicle is stopped at power-up,
 * requires a physical button press, ignores malformed messages, limits actuator
 * outputs, and enters a local fail-safe after 250 ms without a valid command.
 * A fail-safe can be cleared only with another physical button press; a fresh
 * command received after that press is required before motion resumes.
 *
 * 本程序是当前纯视觉架构的比赛候选底层控制器。Orange Pi以ASCII文本行
 * “steer,speed\n”发送命令，两项都必须是-100..100内的整数。车辆上电默认
 * 停止，必须按下物理按钮才允许接收行驶命令；畸形消息会被忽略，执行输出
 * 受到限幅，250 ms内没有合法新命令即进入本地安全停车。故障后必须再次按
 * 物理按钮，并在按键后收到新命令，车辆才可能恢复运动。
 *
 * IMPORTANT / 重要:
 * - Verify motor-driver electrical compatibility before connecting hardware.
 * - Confirm steering sign, motor direction and mechanical servo limits with the
 *   wheels lifted. Change the constants below only from measured results.
 * - This interface is PWM + DIR. A dual-PWM driver needs a different output layer.
 * - 接线前必须核对电机驱动器电气接口；必须架空车轮确认转向正负、电机方向
 *   和舵机机械极限。此版本为PWM+DIR接口，双PWM驱动器不能直接使用。
 */

#include <Servo.h>
#include <stdlib.h>

// Current documented candidate pin map / 当前文档候选引脚
const uint8_t PIN_SERVO = 2;
const uint8_t PIN_MOTOR_PWM = 6;
const uint8_t PIN_MOTOR_DIR = 7;
const uint8_t PIN_START_BUTTON = 8;  // Normally open to GND / 常开按钮接GND

// Conservative initial limits; replace only after lifted-wheel calibration.
// 保守初始限位；仅在架空标定后依据实测修改。
const int SERVO_LEFT_DEG = 45;
const int SERVO_CENTER_DEG = 90;
const int SERVO_RIGHT_DEG = 135;
const uint8_t MAX_MOTOR_PWM = 170;  // 67% of 255 during integration tests

const unsigned long COMMAND_TIMEOUT_MS = 250;
const unsigned long BUTTON_DEBOUNCE_MS = 35;
const unsigned long STATUS_INTERVAL_MS = 500;
const uint8_t RX_BUFFER_SIZE = 24;

enum RobotState : uint8_t {
  WAIT_START = 0,
  VISION_DRIVE = 1,
  COMMS_FAILSAFE = 2
};

Servo steeringServo;
RobotState state = WAIT_START;

char rxBuffer[RX_BUFFER_SIZE];
uint8_t rxLength = 0;
bool rxOverflow = false;

int targetSteer = 0;
int targetSpeed = 0;
bool freshCommandSinceArm = false;
unsigned long lastValidCommandMs = 0;
unsigned long lastStatusMs = 0;

bool lastButtonReading = HIGH;
bool stableButtonState = HIGH;
unsigned long lastButtonChangeMs = 0;

void setSteeringLogical(int command) {
  command = constrain(command, -100, 100);
  int angle;
  if (command < 0) {
    angle = map(command, -100, 0, SERVO_LEFT_DEG, SERVO_CENTER_DEG);
  } else {
    angle = map(command, 0, 100, SERVO_CENTER_DEG, SERVO_RIGHT_DEG);
  }
  steeringServo.write(constrain(angle, SERVO_LEFT_DEG, SERVO_RIGHT_DEG));
}

void setMotorLogical(int command) {
  command = constrain(command, -100, 100);
  const bool forward = command >= 0;
  const uint8_t pwm = (uint8_t)map(abs(command), 0, 100, 0, MAX_MOTOR_PWM);
  digitalWrite(PIN_MOTOR_DIR, forward ? HIGH : LOW);
  analogWrite(PIN_MOTOR_PWM, pwm);
}

void stopActuators() {
  analogWrite(PIN_MOTOR_PWM, 0);
  setSteeringLogical(0);
  targetSteer = 0;
  targetSpeed = 0;
}

void enterWaitStart() {
  stopActuators();
  freshCommandSinceArm = false;
  state = WAIT_START;
  Serial.println(F("STATE,WAIT_START"));
}

void enterFailsafe() {
  stopActuators();
  freshCommandSinceArm = false;
  state = COMMS_FAILSAFE;
  Serial.println(F("STATE,COMMS_FAILSAFE"));
}

bool parseIntegerToken(const char *text, int &value) {
  if (text == NULL || *text == '\0') return false;
  char *endPointer = NULL;
  const long parsed = strtol(text, &endPointer, 10);
  if (*endPointer != '\0' || parsed < -100 || parsed > 100) return false;
  value = (int)parsed;
  return true;
}

bool parseCommandLine(char *line, int &steerOut, int &speedOut) {
  char *comma = strchr(line, ',');
  if (comma == NULL || strchr(comma + 1, ',') != NULL) return false;
  *comma = '\0';
  return parseIntegerToken(line, steerOut) && parseIntegerToken(comma + 1, speedOut);
}

void handleCompleteLine() {
  rxBuffer[rxLength] = '\0';
  int parsedSteer = 0;
  int parsedSpeed = 0;

  if (!rxOverflow && parseCommandLine(rxBuffer, parsedSteer, parsedSpeed)) {
    // Commands received before physical arming are deliberately discarded.
    // 物理启动前收到的命令会被主动丢弃，防止旧命令触发车辆。
    if (state == VISION_DRIVE) {
      targetSteer = parsedSteer;
      targetSpeed = parsedSpeed;
      lastValidCommandMs = millis();
      freshCommandSinceArm = true;
    }
  }

  rxLength = 0;
  rxOverflow = false;
}

void readSerialNonBlocking() {
  while (Serial.available() > 0) {
    const char incoming = (char)Serial.read();
    if (incoming == '\n') {
      handleCompleteLine();
    } else if (incoming != '\r') {
      if (rxLength < RX_BUFFER_SIZE - 1) {
        rxBuffer[rxLength++] = incoming;
      } else {
        rxOverflow = true;
      }
    }
  }
}

bool startButtonPressed() {
  const bool reading = digitalRead(PIN_START_BUTTON);
  if (reading != lastButtonReading) {
    lastButtonReading = reading;
    lastButtonChangeMs = millis();
  }

  if ((millis() - lastButtonChangeMs) >= BUTTON_DEBOUNCE_MS &&
      stableButtonState != reading) {
    stableButtonState = reading;
    return stableButtonState == LOW;
  }
  return false;
}

void handleStartButton() {
  if (!startButtonPressed()) return;

  if (state == VISION_DRIVE) {
    // The same button acts as a local stop while running.
    // 行驶中按同一按钮，立即回到停车等待状态。
    enterWaitStart();
  } else {
    stopActuators();
    freshCommandSinceArm = false;
    lastValidCommandMs = millis();
    state = VISION_DRIVE;
    Serial.println(F("STATE,VISION_DRIVE_ARMED"));
  }
}

void updateStateMachine() {
  if (state == WAIT_START || state == COMMS_FAILSAFE) {
    stopActuators();
    return;
  }

  const unsigned long commandAgeMs = millis() - lastValidCommandMs;
  if (!freshCommandSinceArm) {
    stopActuators();
    if (commandAgeMs > COMMAND_TIMEOUT_MS) enterFailsafe();
    return;
  }

  if (commandAgeMs > COMMAND_TIMEOUT_MS) {
    enterFailsafe();
    return;
  }

  setSteeringLogical(targetSteer);
  setMotorLogical(targetSpeed);
}

void printStatusPeriodically() {
  if (millis() - lastStatusMs < STATUS_INTERVAL_MS) return;
  lastStatusMs = millis();
  Serial.print(F("STATUS,"));
  Serial.print((int)state);
  Serial.print(',');
  Serial.print(targetSteer);
  Serial.print(',');
  Serial.print(targetSpeed);
  Serial.print(',');
  if (state == VISION_DRIVE && freshCommandSinceArm) {
    Serial.println(millis() - lastValidCommandMs);
  } else {
    Serial.println(F("NA"));
  }
}

void setup() {
  pinMode(PIN_MOTOR_PWM, OUTPUT);
  pinMode(PIN_MOTOR_DIR, OUTPUT);
  pinMode(PIN_START_BUTTON, INPUT_PULLUP);

  analogWrite(PIN_MOTOR_PWM, 0);
  digitalWrite(PIN_MOTOR_DIR, LOW);

  steeringServo.attach(PIN_SERVO);
  setSteeringLogical(0);

  Serial.begin(115200);
  Serial.println(F("BSSN_WRO_VISION_EXECUTOR,1.0"));
  enterWaitStart();
}

void loop() {
  readSerialNonBlocking();
  handleStartButton();
  updateStateMachine();
  printStatusPeriodically();
}

