# air_mouse
A simple wireless air mouse using mpu6050 controlled by arduino uno/nano microcontroller and interfaced with my laptop using python.
<br><h2>Hardware Used</h2>
1. Arduino UNO/Nano (one at transmitter and one at receiver)
2. MPU 6050
3. Tactile push button(to simulate left mouse click)
4. 1k ohm pull down resistor
5. 433MHz Transreceiver

<br><h2>Connections</h2>

<h3>Receiver side</h3>
<b>433MHz receiver-----Arduino</b><br>
VCC--------------------5V<br>
GND--------------------GND<br>
Data pin---------------Pin 11
<h3>Transmitter side</h3>
<b>433MHz Transmitter--Arduino</b><br>
VCC--------------------5V<br>
GND--------------------GND<br>
Data pin---------------Pin 12<br>
<b>MPU 6050------------Arduino</b><br>
VCC--------------------5V<br>
GND--------------------GND<br>
SCL--------------------A5<br>
SDA--------------------A4<br>
<b>Tactile button------Arduino</b><br>
One end----------------5V<br>
Other end--------------D6<br>
Pull down resistor D6 to ground

<br><h2>Explanation</h2>
The mpu and button pressed data is read by arduino and transmitted using the 433MHz ttranmitter. The receiver receives the data and the arduino unpacks it to be used by python program. The mpu's x and y acceleration is used to determine how much it is tilted and python read this data through serial port and convert it into equivalent cursor movement.
The cursor movement can be tuned by changing the deadzone and speed multiplier defined in python code.

<br><h2>Modifications that can be done</h2>
Replacing the arduino with esp32 will be great as the 433MHz transreceiver can be replaced by inbuilt esp32's bluetooth. This will reduce the latency and hardware as well.