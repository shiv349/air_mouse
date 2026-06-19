import time
import pyautogui
import serial

# --- CONFIGURATION ---
SERIAL_PORT = "/dev/cu.usbserial-10"  #Serial port address
BAUD_RATE = 115200  #Same as defined for arduino

# Deadzone Thresholds (helpfull for ignoring minor tilts)
X_DEADZONE_MIN, X_DEADZONE_MAX = -2.0, 2.0
Y_DEADZONE_MIN, Y_DEADZONE_MAX = -1.0, 1.0
SPEED_MULTIPLIER = 14   #Determines how fast the cursor will react

pyautogui.FAILSAFE = False

# Prevents holding the physical button down from spamming continuous clicks
button_was_pressed = False

# --- SERIAL INITIALIZATION ---
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print(f"Connected to {SERIAL_PORT} successfully.")
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit()


def process_accelerometer_data(x_val, y_val):
    # Applies deadzone logic and calculates cursor movement
    move_x = 0
    move_y = 0

    if x_val > X_DEADZONE_MAX:
        move_x = -(x_val - X_DEADZONE_MAX) * SPEED_MULTIPLIER
    elif x_val < X_DEADZONE_MIN:
        move_x = -(x_val - X_DEADZONE_MIN) * SPEED_MULTIPLIER

    if y_val > Y_DEADZONE_MAX:
        move_y = -(y_val - Y_DEADZONE_MAX) * SPEED_MULTIPLIER
    elif y_val < Y_DEADZONE_MIN:
        move_y = -(y_val - Y_DEADZONE_MIN) * SPEED_MULTIPLIER

    return int(move_x), int(move_y)


# --- MAIN LOOP ---
try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").strip()

            try:
                # Expecting 3 values now: "x_val,y_val,button_state"
                parts = line.split(",")
                if len(parts) == 3:
                    acc_x = float(parts[0])
                    acc_y = float(parts[1])
                    btn_state = int(parts[2])  # 1 for pressed, 0 for released

                    # Handle Cursor Movement
                    dx, dy = process_accelerometer_data(acc_x, acc_y)
                    if dx != 0 or dy != 0:
                        pyautogui.moveRel(dx, dy)

                    # Handle Left Click Logic (Edge Triggered)
                    if btn_state == 1 and not button_was_pressed:
                        pyautogui.leftClick()
                        button_was_pressed = True  # Lock until button is released
                    elif btn_state == 0:
                        button_was_pressed = False  # Unlock when button is released

            except ValueError:
                pass

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")
finally:
    ser.close()
    print("Serial port closed.")