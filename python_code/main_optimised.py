import sys
import time
import pyautogui
import serial

SERIAL_PORT = "/dev/cu.usbserial-10"
BAUD_RATE = 115200

# Tuning parameters
SENSITIVITY = 40 
ALPHA = 0.98        

angle_x = 0.0
angle_y = 0.0
prev_time = time.time()
prev_click_state = 0

pyautogui.FAILSAFE = False

print(f"Connecting to {SERIAL_PORT}...")

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.001)
    print("Connected! High-speed low-lag mode active.")

    while True:
        if ser.in_waiting > 100:
            ser.reset_input_buffer()

        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8", errors="ignore").strip()

            try:
                # Expecting: gyro_x, gyro_y, acc_x, acc_y, click
                g_x, g_y, a_x, a_y, click_str = line.split(",")
                
                gyro_x = float(g_x)
                gyro_y = float(g_y)
                acc_x = float(a_x)
                acc_y = float(a_y)
                click_state = int(click_str)

                current_time = time.time()
                dt = current_time - prev_time
                prev_time = current_time

                # Guard against tiny or zero dt to avoid division errors
                if dt < 0.001:
                    dt = 0.001

                # Filter math
                import math
                acc_angle_x = math.atan2(acc_y, math.sqrt(acc_x**2 + 1.0)) * (180.0 / math.pi)
                acc_angle_y = math.atan2(-acc_x, math.sqrt(acc_y**2 + 1.0)) * (180.0 / math.pi)

                angle_x = ALPHA * (angle_x + gyro_x * dt) + (1.0 - ALPHA) * acc_angle_x
                angle_y = ALPHA * (angle_y + gyro_y * dt) + (1.0 - ALPHA) * acc_angle_y

                # Calculate movement based on the real-time dt step
                move_x = -int(gyro_x * SENSITIVITY * dt) 
                move_y = -int(gyro_y * SENSITIVITY * dt)

                if abs(move_x) < 3: move_x = 0
                if abs(move_y) < 2: move_y = 0

                if move_x != 0 or move_y != 0:
                    pyautogui.moveRel(move_x, move_y)

                if click_state == 1 and prev_click_state == 0:
                    pyautogui.click()
                prev_click_state = click_state

            except (ValueError, ZeroDivisionError):
                continue

except serial.SerialException:
    print(f"Error: Could not open serial port {SERIAL_PORT}.")
except KeyboardInterrupt:
    print("\nProgram stopped.")
    sys.exit()
