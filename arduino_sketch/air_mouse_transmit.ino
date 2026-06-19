#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <RH_ASK.h> // RadioHead ASK Library for transmitter setup
#include <SPI.h>    // Required by RadioHead

const int BUTTON_PIN = 6; // Pin connected to the button

Adafruit_MPU6050 mpu;
RH_ASK driver(2000, 11, 12, 10); // Speed: 2000 bps, RX pin 11, TX pin 12

// Define a compact structure to hold only the essential motion data
struct MotionData {
  float accX;
  float accY;
  uint8_t buttonPressed;
};

void setup() {
  Serial.begin(115200);
  
  pinMode(BUTTON_PIN, INPUT); 
  
  if (!mpu.begin()) {
    Serial.println("MPU6050 missing!");
    while (1);
  }
  
  if (!driver.init()) {
    Serial.println("RF Transmitter init failed!");
    while (1);
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Pack current readings into the structure
  MotionData data;
  data.accX = a.acceleration.x;
  data.accY = a.acceleration.y;
  
  // Read button state
  if (digitalRead(BUTTON_PIN) == HIGH) {
    data.buttonPressed = 1;
  } else {
    data.buttonPressed = 0;
  }

  // Send the structure as a raw byte array
  driver.send((uint8_t *)&data, sizeof(data));
  driver.waitPacketSent();

  delay(30); // Small delay to prevent flooding the airwaves
}
