import sys
import json
import pandas as pd
import RPi.GPIO as GPIO
import ADS1256
import load_cells

def main():
    # Create an instance of the ADS1256 class
    ads = ADS1256()

    # Calibration factors are the slope and intercept to convert raw ADC readings to weight
    calibration_factors = {
        "Differential 0-1": (0.005255402508804553, -32.77118234095868),
        "Differential 2-3": (0.0064694839574558245, -35.8680578828282),
        "Differential 4-5": (0.006428018984246993, -134.56260257211812),
        "Differential 6-7": (0.008134870987764936, -49.37097264202684),
    }

    # # Read from JSON file
    # with open('calibration.json', 'r') as json_file:
    #     data = json.load(json_file)

    # # Convert lists to tuples
    # calibration_factors = {key: tuple(value) for key, value in data.items()}

    try:
        # Check if the command-line argument 'calibrate' is passed
        if len(sys.argv) > 1 and sys.argv[1] == 'calibrate':
            print("Starting calibration...")
            ads.calibrate()
            return

        # Read voltages from load cells
        voltages = load_cells.read_voltages(ads)

        # This is what needs to change depending on the output.
        
        # Convert voltages to weights using the calibration factors
        weights_dict = load_cells.convert_voltages_to_weights(voltages, calibration_factors)
        
        # Create a DataFrame from the weights data and save to CSV
        df_weights = pd.DataFrame.from_dict(weights_dict, orient='index').transpose()
        df_weights.to_csv('load_cell_weights.csv', index=False)
        print("Weights saved to 'load_cell_weights.csv'.")
    
    except Exception as e:
        print(f"Error: {e}")
        GPIO.cleanup()

if __name__ == "__main__":
    main()

# Next steps...
# Create output functionaility
# Rewrite the calibration script
# Finish main.py
    # Use a JSON file to store the calibration factors
    # Write to that JSON file in the calibration script
    # main.py will read from that JSON file at runtime