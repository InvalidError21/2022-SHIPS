nclude <Servo.h>

Servo propL; // 프로펠러 좌우 설정
Servo propR;
int L = 9;
int R = 10;

int ch1; // 수신기 채널 (총 6개 채널 중 홀수 채널만 data 있음, 짝수 채널 미설정시 해당 채널 이후 홀수 채널도 안들어옴)
int ch2;
int ch3;

int LPWM;
int RPWM;

void setup() {
  pinMode(3, INPUT);
  pinMode(5, INPUT);
  pinMode(6, INPUT);
  propL.attach(L);
  propR.attach(R);
  Serial.begin(9600);

  propL.writeMicroseconds(1500); // 프로펠러 대기
  propR.writeMicroseconds(1500);

  delay(5000);
}

void loop() {
  ch1 = pulseIn(3, HIGH, 25000); // 채널별 펄스값
  ch2 = pulseIn(5, HIGH, 25000);
  ch3 = pulseIn(6, HIGH, 25000);

  LPWM = ch3 + 20;
  RPWM = ch1 + 10;

  if (LPWM > 1900) LPWM = 1100; // 펄스값 구간 설정 (프로펠러 1500 = 정지, 1100/1900 = 역/정방향 최대치), ch1 역회전/ch3 정회전 = 전진
  else if (1500 < LPWM < 1900) LPWM = 1500 - (LPWM - 1500);
  else if (1100 < LPWM < 1500) LPWM = 1500 + (1500 - LPWM);
  else if (LPWM < 1100) LPWM = 1900;
  
  if (RPWM > 1900) RPWM = 1900;
  else if (RPWM < 1100) RPWM = 1100;

  Serial.print("Channel 1:"); // 채널값 확인
  Serial.println(RPWM);

  Serial.print("Channel 3:");
  Serial.println(LPWM);

  propL.writeMicroseconds(RPWM);
  propR.writeMicroseconds(LPWM);
  delay(10);
}
