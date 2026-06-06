#include <Servo.h>

// 超声波引脚
#define TRIG_PIN 3  // 发射脚 T
#define ECHO_PIN 4  // 接收脚 E

// ===================== 引脚与参数设置 =====================
#define STEER_PIN 2         // 转向舵机端口
const int MIN_ANGLE = 35;   // 最左角度（对应 -100）
const int MAX_ANGLE = 145;  // 最右角度（对应 100）

// 电机驱动引脚
#define PWM_PIN 6
#define DIR_PIN 7
// ==========================================================

// 全局定义舵机对象
Servo steeringServo;

// 全局变量（用于串口显示）
int currentSteer = 0;          // 当前舵机转向值
int currentSpeed = 0;          // 当前电机速度
String currentState = "待机";  // 当前状态

// ===================== 超声波测距函数（带异常过滤） =====================
float getDistance(void) {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long t = pulseIn(ECHO_PIN, HIGH, 30000);  // 超时30ms（约5米）
  if (t == 0) return 999;                   // 检测不到返回999cm（视为无限远）

  float dis = t * 0.034 / 2.0;
  return dis;
}

// ===================== 电机控制函数 =====================
void move(int speed) {
  currentSpeed = speed;  // 记录当前速度

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

// ===================== 转向控制函数 =====================
void steer(int steerValue) {
  currentSteer = steerValue;  // 记录当前转向值

  int targetAngle = map(steerValue, -100, 100, MIN_ANGLE, MAX_ANGLE);
  targetAngle = constrain(targetAngle, MIN_ANGLE, MAX_ANGLE);
  steeringServo.write(targetAngle);
}

// ===================== 初始化 =====================
void setup() {
  steeringServo.attach(STEER_PIN);
  pinMode(PWM_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  Serial.begin(9600);  // 开启串口通讯
  Serial.println("阿克曼小车启动成功！");
  Serial.println("------------------------");
}

// ===================== 主循环（完全符合你的需求） =====================
void loop() {
  float distance = getDistance();

  // 核心控制逻辑
  if (distance >= 70) {
    // 前方通畅：直行前进
    currentState = "直行前进";
    steer(0);
    move(50);
  } else {
    // 检测到障碍物：开始避障流程
    currentState = "避障转弯中";
    move(0);          // 先紧急停车
    delay(100);       // 刹车缓冲

    // 第一步：一直转弯，直到前方距离≥70cm
    while (distance < 80) {
      steer(90);    // 
      move(90);       // 低速转弯（建议30-50，太快容易打滑）
      distance = getDistance();  // 实时更新距离
      
      // 转弯过程中也实时打印数据
      Serial.print("距离: ");
      Serial.print(distance);
      Serial.print(" cm | 状态: ");
      Serial.print(currentState);
      Serial.print(" | 转向: ");
      Serial.print(currentSteer);
      Serial.print(" | 速度: ");
      Serial.println(currentSpeed);
      
      delay(50);
    }

    // 第二步：前方已经通畅，再额外多转0.5秒（你的核心需求）
    currentState = "额外转弯0.5秒";
    delay(500);

    // 第三步：避障完成，回正舵机准备继续直行
    steer(0);
    move(0);
    delay(200);       // 回正缓冲
  }

  // 正常行驶时的实时串口数据显示
  if (currentState == "直行前进") {
    Serial.print("距离: ");
    Serial.print(distance);
    Serial.print(" cm | 状态: ");
    Serial.print(currentState);
    Serial.print(" | 转向: ");
    Serial.print(currentSteer);
    Serial.print(" | 速度: ");
    Serial.println(currentSpeed);
  }

  delay(50);
}