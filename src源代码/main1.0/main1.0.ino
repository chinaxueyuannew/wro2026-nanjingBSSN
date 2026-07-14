#include <Servo.h>

// ===================== 超声波引脚 =====================
#define TRIG_F  3   // 前方超声波 发射
#define ECHO_F  4   // 前方超声波 接收
#define TRIG_R  8   // 右侧超声波 发射
#define ECHO_R  9   // 右侧超声波 接收

// ===================== 引脚与参数设置 =====================
#define STEER_PIN 2
const int MIN_ANGLE = 35;   // 最左角度（对应 steer -100）
const int MAX_ANGLE = 145;  // 最右角度（对应 steer +100）

#define PWM_PIN 6
#define DIR_PIN 7

// ===================== 巡墙 P 控制参数 =====================
const float TARGET_DIST = 30.0;  // 目标右侧距离（cm）
const float KP          = 2.5;   // 比例系数，可调
const int   DRIVE_SPEED = 70;    // 前进速度
const int   MAX_STEER   = 90;    // 最大转向幅度（限幅，防打死）

// ===================== 全局对象 =====================
Servo steeringServo;

int   currentSteer = 0;
int   currentSpeed = 0;
const char* currentState = "巡墙前进";

// ===================== 超声波测距 =====================
float getDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long t = pulseIn(echoPin, HIGH, 30000);
  if (t == 0) return 999;
  return t * 0.034 / 2.0;
}

// ===================== 电机控制 =====================
void move(int speed) {
  currentSpeed = speed;
  if (speed > 0) {
    digitalWrite(DIR_PIN, HIGH);
    analogWrite(PWM_PIN, speed * 2.55);
  } else if (speed < 0) {
    digitalWrite(DIR_PIN, LOW);
    analogWrite(PWM_PIN, -speed * 2.55);
  } else {
    analogWrite(PWM_PIN, 0);
  }
}

// ===================== 转向控制 =====================
void steer(int steerValue) {
  currentSteer = steerValue;
  int angle = map(steerValue, -100, 100, MIN_ANGLE, MAX_ANGLE);
  angle = constrain(angle, MIN_ANGLE, MAX_ANGLE);
  steeringServo.write(angle);
}

// ===================== 初始化 =====================
void setup() {
  steeringServo.attach(STEER_PIN);
  steeringServo.write(map(0, -100, 100, MIN_ANGLE, MAX_ANGLE));

  pinMode(PWM_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(TRIG_F, OUTPUT);
  pinMode(ECHO_F, INPUT);
  pinMode(TRIG_R, OUTPUT);
  pinMode(ECHO_R, INPUT);

  move(0);

  Serial.begin(9600);
  Serial.println("=======================================");
  Serial.println("  阿克曼小车 - 右侧巡墙模式 (P控制)");
  Serial.println("  目标距离: 30cm  速度: 80  KP: 2.0");
  Serial.println("=======================================");
  Serial.println("前方(cm) | 右侧(cm) | 误差(cm) | 转向 | 速度");
  Serial.println("-------------------------------------------------");
}

// ===================== 主循环 =====================
void loop() {
  float distFront = getDistance(TRIG_F, ECHO_F);
  float distRight = getDistance(TRIG_R, ECHO_R);

  // ---------- P 控制计算转向 ----------
  // 误差 = 实际距离 - 目标距离
  // 误差 > 0（偏远）→ 右转（正值）
  // 误差 < 0（偏近）→ 左转（负值）
  float error = 0;
  int   steerOut = 0;

  if (distRight < 500) {  // 右侧有效读数才做控制
    error    = distRight - TARGET_DIST;
    steerOut = (int)(KP * error);
    steerOut = constrain(steerOut, -MAX_STEER, MAX_STEER);
  }
  // 右侧无读数时保持直行
  steer(steerOut);
  move(DRIVE_SPEED);

  // ---------- 串口实时输出 ----------
  Serial.print("前方: ");
  Serial.print(distFront >= 999 ? 999 : distFront, 1);
  Serial.print(" cm | 右侧: ");
  Serial.print(distRight >= 999 ? 999 : distRight, 1);
  Serial.print(" cm | 误差: ");
  Serial.print(error, 1);
  Serial.print(" cm | 转向: ");
  Serial.print(currentSteer);
  Serial.print(" | 速度: ");
  Serial.println(currentSpeed);

  delay(50);  // 50ms 控制周期
}
