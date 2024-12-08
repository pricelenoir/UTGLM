import serial
import time

def main():
    # Configuration port and baud rate
    SERIAL_PORT = '/dev/ttyUSB0'
    BAUD_RATE = 115200
    CONFIG_FILE = 'IWR6843ISK.cfg'

    with open(CONFIG_FILE, 'r') as file:
        config = file.readlines()

    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
    if ser.is_open:
        print(f"Connected to {SERIAL_PORT}")
    else:
        print("Error. Serial port is not open.")
        return
        
    for line in config:
        line = line.strip()
        if not line or line.startswith("%"):
            continue

        ser.write((line + '\n').encode('utf-8'))
        time.sleep(0.1)
        response = ser.readline().decode('utf-8').strip()

        if response.startswith(("Skipped", "Done", "Ignored", "sensorStop", "mmwDemo")):
            continue

        if response:
            print(response)

    print("Configuration complete.")
    return

if __name__ == "__main__":
    main()