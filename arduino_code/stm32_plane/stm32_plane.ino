#include<Wire.h>
#include<Servo.h>
#include <TinyGPS.h>

#define BMP180_ADDRESS 0x77   // BMP180 주소
#define MPU6050_ADDRESS 0x68  // mpu6050 주소
#define QMC5883_ADDRESS 0x0D  // qmc5883 주소
#define RF24_ADDRESS 0x01     // rf24 아두이노 주소

#define Cal_Data 2024
#define Max_Signal 2000
#deiine Min_Signal 1000

struct Drone_Angle{
  float AngleX = 0, AngleY = 0, AngleZ = 0;
};

struct PID{
  float P, I, D;
  float I_last;
  float err_last;
};

struct Position{
  int32_t Alt_pressure = 0;
  float Lat = 0, Lon = 0, Alt = 0;
  float Pow = 0;
};

Servo Motor1;
TinyGPS Gps;

Drone_Angle Angles;
Drone_Angle T_Angles;

void setup() {
  Reset();
}

void loop() {
  // put your main code here, to run repeatedly:

}
