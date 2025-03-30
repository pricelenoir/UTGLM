import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
import json
import os

def calibrate(ads):
    weights = [0, 5, 10, 25, 50]  # Example weights in pounds
    calibration_results = {}
    
    # Define differential channel pairs with their names
    diff_channels = {
        0: "Differential 0-1",
        1: "Differential 2-3",
        2: "Differential 4-5",
        3: "Differential 6-7"
    }
    
    # Collect data for each differential channel pair
    for ch_pair in range(4):
        channel_name = diff_channels[ch_pair]
        print(f"\nCalibrating {channel_name}...")
        adc_values = []
        
        for weight in weights:
            input(f"Place {weight} pounds on load cell for {channel_name} and press 'Enter'.")
            raw_adc_value = ads.get_diff_channel_value(ch_pair)
            adc_values.append(raw_adc_value)
            print(f"Weight: {weight} lbs - ADC value: {raw_adc_value}")
        
        # Perform linear regression for this channel
        slope, intercept, r_value, p_value, std_err = linregress(adc_values, weights)
        
        # Store calibration parameters
        calibration_results[channel_name] = [slope, intercept]
        
        # Display calibration results for this channel
        print(f"Calibration for {channel_name}:")
        print(f"Equation: weight = ({slope:.6f} * ADC Value) + {intercept:.6f}")
        print(f"R-squared: {r_value**2:.6f}")
        
        # Plot calibration curve for this channel
        plt.figure(figsize=(10, 6))
        plt.scatter(adc_values, weights, color='blue', label='Calibration Data')
        plt.plot(adc_values, [slope * x + intercept for x in adc_values], color='red', label='Fitted Line')
        
        plt.title(f'Load Cell Calibration Curve - {channel_name}')
        plt.xlabel('ADC Value')
        plt.ylabel('Weight (pounds)')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    # Write calibration parameters to JSON file
    with open('calibration.json', 'w') as json_file:
        json.dump(calibration_results, json_file, indent=4)
    
    print("\nCalibration complete! Parameters saved to 'calibration.json'")
    
    return calibration_results