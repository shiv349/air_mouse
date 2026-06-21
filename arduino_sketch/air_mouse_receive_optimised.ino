#include <RH_ASK.h>
#include <SPI.h> 

RH_ASK driver(2000, 11, 12, 10); // Speed: 2000 bps, RX pin 11, TX pin 12

struct MotionData {
  int16_t accX;
  int16_t accY;
  int16_t gyroX;
  int16_t gyroY;
  uint8_t buttonPressed;
};

void setup() {
  Serial.begin(115200);
  if (!driver.init()) {
    Serial.println("RF Receiver init failed!");
    while (1);
  }
}

void loop() {
  MotionData receivedData;
  uint8_t buflen = sizeof(receivedData);

  // Check if a valid radio packet of the correct size has arrived
  if (driver.recv((uint8_t *)&receivedData, &buflen)) {
    float actualX = receivedData.accX / 100.0;
    float actualY = receivedData.accY / 100.0;
    float actualXg = receivedData.gyroX / 100.0;
    float actualYg = receivedData.gyroY / 100.0;
    
    // Print in the precise comma-separated string format expected by Python
    Serial.print(actualX, 2);
    Serial.print(",");
    Serial.print(actualY, 2);
    Serial.print(",");
    Serial.print(actualXg, 2);
    Serial.print(",");
    Serial.print(actualYg, 2);
    Serial.print(",");
    Serial.println(receivedData.buttonPressed);
  }
}
