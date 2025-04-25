import sys
import json
import tkinter as tk
import RPi.GPIO as GPIO
from src.calibrate import calibrate
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
        calibrate(ads)
        return

    # Read calibration factors and zero load offsets from JSON
    with open('calibration.json', 'r') as json_file:
        data = json.load(json_file)
    
    calibration_factors = data['calibration_factors']  # Now calibration_factors is just {key: slope}
    zero_load_offsets = data['zero_load_offsets']

    # Create Tkinter root and weight balance board GUI
    root = tk.Tk()
    root.configure(bg='black')
    root.title("Golf Swing Balance Analyzer - Testing Mode")
    weight_board = WeightBalanceBoard(root)

    try:
        def update_gui():
            # Read ADC values from load cells
            adc_values = load_cells.read_adc_values(ads)
            
            # Convert ADC values to weights using calibration factors
            weights_dict = load_cells.convert_adc_to_weights(adc_values, calibration_factors, zero_load_offsets)
            
            # Update visualization
            weight_board.update_visualization(adc_values, weights_dict)
            root.after(100, update_gui)  # Update every 100 ms

        # Start the update loop and Tkinter event loop
        update_gui()
        root.mainloop()

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
