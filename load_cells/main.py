import sys
import json
import tkinter as tk
import RPi.GPIO as GPIO
from src import load_cells
from src.ADS1256 import ADS1256
from src.weight_balance_gui import WeightBalanceBoard

def main():
    # Create an instance of the ADS1256 class
    ads = ADS1256()
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

    # Create Tkinter root and weight balance board GUI
    root = tk.Tk()
    weight_board = WeightBalanceBoard(root)

    try:
        def update_gui():
            # Read voltages from load cells
            voltages = load_cells.read_voltages(ads)
            
            # Convert voltages to weights using calibration factors
            weights_dict = load_cells.convert_voltages_to_weights(voltages, calibration_factors)
            
            # Update visualization
            weight_board.update_visualization(voltages, weights_dict)
            root.after(100, update_gui)  # Update every 100 ms

        # Start the update loop and Tkinter event loop
        update_gui()
        root.mainloop()

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
