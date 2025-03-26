import sys
import json
import pandas as pd
import RPi.GPIO as GPIO
from src import ADS1256
from src import load_cells

def main():
    # Create an instance of the ADS1256 class
    ads = ADS1256.ADS1256()
    ads.initialize()

    # Check if the command-line argument 'calibrate' is passed
    if len(sys.argv) > 1 and sys.argv[1] == 'calibrate':
        print("Starting calibration...")
        ads.calibrate()
        print("Calibration complete.")
        return

    # Read calibration factors from JSON (the slope and intercept to convert raw ADC readings to weight)
    with open('calibration.json', 'r') as json_file:
        data = json.load(json_file)
    calibration_factors = {key: tuple(value) for key, value in data.items()}

    try:
        while True:
            # Read voltages from load cells
            voltages = load_cells.read_voltages(ads)
            
            # Convert voltages to weights using the calibration factors
            weights_dict = load_cells.convert_voltages_to_weights(voltages, calibration_factors)
            print(weights_dict)
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
