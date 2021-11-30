#include <MPU6050_tockn.h>
#include <Wire.h>

MPU6050 mpu6050(Wire);

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
}
void print_begin() {
  Serial.print("{");
}
void print_sep() {
  Serial.print(",");
}
void print_end() {
  Serial.println("\"}");
}
void print_angle() {
  Serial.print("\"AngleX\":\"");
  Serial.print(mpu6050.getAngleX());
  Serial.print("\",\"AngleY\":\"");
  Serial.print(mpu6050.getAngleY());
  Serial.print("\",\"AngleZ\":\"");
  Serial.print(mpu6050.getAngleZ());
}
void print_acc() {
  Serial.print("\"AccX\":\"");
  Serial.print(mpu6050.getAccX());
  Serial.print("\",\"AccY\":\"");
  Serial.print(mpu6050.getAccY());
  Serial.print("\",\"AccZ\":\"");
  Serial.print(mpu6050.getAccZ());
}
void print_all_data() {
  print_begin();
  print_acc();
  print_sep();
  print_angle();
  print_end();
}

void loop() {
  mpu6050.update();
  print_all_data();
}
