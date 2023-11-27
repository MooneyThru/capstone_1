#include <Arduino.h>
#include <Servo.h>

// 모터 관련 변수 및 상수
volatile int encoderCount1 = 0;
volatile unsigned long lastTime1 = 0;
volatile int motorRPM1 = 0;
volatile int encoderCount2 = 0;
volatile unsigned long lastTime2 = 0;
volatile int motorRPM2 = 0;
const int cpr = 64;  
const int gearRatio = 150;  

// 엔코더 핀
const int encoderPinA1 = 2; 
const int encoderPinB1 = 3;
const int encoderPinA2 = 20;
const int encoderPinB2 = 21;

// 모터 제어 핀
const int motorSpeedPin1 = 7; 
const int motorDirection1_1 = 8;
const int motorDirection2_1 = 9;
const int motorSpeedPin2 = 10;
const int motorDirection1_2 = 12;
const int motorDirection2_2 = 13;

// PI 제어 매개변수
const float Kp1 = 1.7, Ki1 = 2.8, Kp2 = 2.0, Ki2 = 1.9;
float errorSum1 = 0, errorSum2 = 0;

// 목표 RPM
volatile int targetRPM_left = 0;
volatile int targetRPM_right = 0;

// 서보 모터
Servo myservo1, myservo2, myservo3, myservo4;

// 그리퍼 : 1 ~ 맨 밑 서보 모터가 4
int current_angle1 = 90, current_angle2 = 0, current_angle3 = 90, current_angle4 = 120;
unsigned long lastUpdate1, lastUpdate2, lastUpdate3, lastUpdate4;

// 모터 RPM 제어 함수
void setMotorDirectionAndSpeed(int motorNumber, int rpm) {
  bool direction = rpm >= 0; // RPM이 양수 또는 0이면 true, 음수면 false
  int speedValue = abs(rpm); // 속도 값은 RPM의 절대값
  if (motorNumber == 1) {
    digitalWrite(motorDirection1_1, direction ? LOW : HIGH);
    digitalWrite(motorDirection2_1, direction ? HIGH : LOW);
    analogWrite(motorSpeedPin1, constrain(speedValue, 0, 255));
  } else if (motorNumber == 2) {
    digitalWrite(motorDirection1_2, direction ? LOW : HIGH);
    digitalWrite(motorDirection2_2, direction ? HIGH : LOW);
    analogWrite(motorSpeedPin2, constrain(speedValue, 0, 255));
  }
}

void setup() {
  // 모터 및 서보 초기 설정
  Serial.begin(9600);
  
  pinMode(encoderPinA1, INPUT);
  pinMode(encoderPinB1, INPUT);
  pinMode(encoderPinA2, INPUT);
  pinMode(encoderPinB2, INPUT);

  attachInterrupt(digitalPinToInterrupt(encoderPinA1), countEncoder1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderPinB1), countEncoder1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderPinA2), countEncoder2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderPinB2), countEncoder2, CHANGE);

  pinMode(motorSpeedPin1, OUTPUT);
  pinMode(motorDirection1_1, OUTPUT);
  pinMode(motorDirection2_1, OUTPUT);
  pinMode(motorSpeedPin2, OUTPUT);
  pinMode(motorDirection1_2, OUTPUT);
  pinMode(motorDirection2_2, OUTPUT);

  digitalWrite(motorDirection1_1, LOW);
  digitalWrite(motorDirection2_1, HIGH);
  analogWrite(motorSpeedPin1, 0);
  digitalWrite(motorDirection1_2, LOW);
  digitalWrite(motorDirection2_2, HIGH);
  analogWrite(motorSpeedPin2, 0);

  myservo1.attach(31);
  myservo2.attach(6);
  myservo3.attach(4);
  myservo4.attach(5);
  
  myservo1.write(current_angle1);
  myservo2.write(current_angle2);
  myservo3.write(current_angle3);
  myservo4.write(current_angle4);
}

void loop() {
  // 시리얼 데이터 처리
  if (Serial.available() > 0) {
  String command = Serial.readStringUntil('\n');
  if (command.startsWith("M")) {
    int motorNumber = command.charAt(1) - '0';
    int rpm = command.substring(2).toInt();

    if (motorNumber == 1) {
      if (rpm >= 0) {
        targetRPM_left = rpm;
      } else { // rpm < 0
        setMotorDirectionAndSpeed(1, rpm); // 모터 방향 및 속도 설정
      }
    } else if (motorNumber == 2) {
      if (rpm >= 0) {
        targetRPM_right = rpm;
      } else { // rpm < 0
       setMotorDirectionAndSpeed(2, rpm); // 모터 방향 및 속도 설정
      }  
      }
    } else if (command.startsWith("S")) {
    int servoNumber = command.charAt(1) - '0';
    int angle = command.substring(2).toInt();
    setServoAngle(servoNumber, angle);
    }
  }

  // 모터 RPM 제어 로직
  // [여기에 모터 RPM 제어 관련 코드를 추가하세요]
  // 1초에 한 번 RPM을 계산하고 표시 (모터 1)
  unsigned long currentTime1 = millis();

  if (currentTime1 - lastTime1 >= 100) {
    // RPM 계산: (펄스 수 / CPR) * 60 * gearRatio
    motorRPM1 = ((abs(encoderCount1) / cpr) * 600 ) / gearRatio;
    Serial.println("Motor 1 RPM: " + String(motorRPM1));

    // PI 제어
    float error1 = targetRPM_left - motorRPM1;
    errorSum1 += error1;

    // PID 제어 신호 계산
    int controlSignal1 = Kp1 * error1 + Ki1 * errorSum1;

    // 제어 신호를 모터에 전달
    analogWrite(motorSpeedPin1, constrain(controlSignal1, 0, 255));

    // 변수 초기화
    encoderCount1 = 0;
    lastTime1 = currentTime1;
  }

  // 1초에 한 번 RPM을 계산하고 표시 (모터 2)
  unsigned long currentTime2 = millis();

  if (currentTime2 - lastTime2 >= 100) {
    // RPM 계산: (펄스 수 / CPR) * 60 * gearRatio
    motorRPM2 = ((abs(encoderCount2) / cpr) * 600 ) / gearRatio;
    Serial.println("Motor 2 RPM: " + String(motorRPM2));

    // PI 제어
    float error2 = targetRPM_right - motorRPM2;
    errorSum2 += error2;

    // PID 제어 신호 계산
    int controlSignal2 = Kp2 * error2 + Ki2 * errorSum2;

    // 제어 신호를 모터에 전달
    analogWrite(motorSpeedPin2, constrain(controlSignal2, 0, 255));

    // 변수 초기화
    encoderCount2 = 0;
    lastTime2 = currentTime2;
  }
}

void setServoAngle(int servoNumber, int angle) {
    switch (servoNumber) {
      case 1:
        for (int pos1 = current_angle1; pos1 != angle; pos1 += (angle > current_angle1) ? 1 : -1) {
          myservo1.write(pos1);
          delay(20);
        }
        myservo1.write(angle);
        current_angle1 = angle;
        break;
      case 2:
        for (int pos2 = current_angle2; pos2 != angle; pos2 += (angle > current_angle2) ? 1 : -1) {
          myservo2.write(pos2);
          delay(20);
        }
        myservo2.write(angle);
        current_angle2 = angle;
        break;
      case 3:
        for (int pos3 = current_angle3; pos3 != angle; pos3 += (angle > current_angle3) ? 1 : -1) {
          myservo3.write(pos3);
          delay(20);
        }
        myservo3.write(angle);
        current_angle3 = angle;
        break;
      case 4:
        for (int pos4 = current_angle4; pos4 != angle; pos4 += (angle > current_angle4) ? 1 : -1) {
          myservo4.write(pos4);
          delay(20);
        }
        myservo4.write(angle);
        current_angle4 = angle;
        break;
      default:
        Serial.println("Invalid servo number");
      }
}

// 엔코더 카운트 함수 (모터 1)
void countEncoder1() {
  encoderCount1++;
}

// 엔코더 카운트 함수 (모터 2)
void countEncoder2() {
  encoderCount2++;
}