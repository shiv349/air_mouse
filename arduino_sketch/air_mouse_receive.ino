#include <RH_ASK.h> // RadioHead ASK Library for transmitter setup
#include <SPI.h>    // Required by RadioHead

RH_ASK driver(2000, 11, 12, 10); // Speed: 2000 bps, RX pin 11, TX pin 12

// Structure exactly same as the transmitter's structure
struct MotionData {
  float accX;
  float accY;
  uint8_t buttonPressed;
};

void setup() {
  Serial.begin(115200);
  if (!driver.init()) {
    Serial.println("RF Receiver init failed!");
    while (1);
  }
  Serial.println("Receiver Ready. Listening for data...");
}

void loop() {
  MotionData receivedData;
  uint8_t buflen = sizeof(receivedData);

  // Check if a valid radio packet of the correct size has arrived
  if (driver.recv((uint8_t *)&receivedData, &buflen)) {
    
    /* Print Unpacked Acceleration Data */
    Serial.print(receivedData.accX, 2);
    Serial.print(",");
    Serial.print(receivedData.accY, 2);
    Serial.print(",");
    Serial.println(receivedData.buttonPressed);
  }
}
