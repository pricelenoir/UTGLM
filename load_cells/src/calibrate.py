import json
import numpy as np
from scipy.stats import linregress

def calibrate(ads):
    weights = [0, 2.5, 5, 10, 15, 20, 25, 30]  # Calibration weights in pounds

    calibration_factors = {}
    zero_load_offsets = {}

    diff_channels = {
        0: "Differential 0-1",
        1: "Differential 2-3",
        2: "Differential 4-5",
        3: "Differential 6-7"
    }
    
    for ch_pair in range(4):
        channel_name = diff_channels[ch_pair]
        print(f"\nCalibrating {channel_name}...")
        adc_values = []
        
        for i, weight in enumerate(weights):
            input(f"Place {weight} pounds on load cell for {channel_name} and press 'Enter'.")

            # Take multiple readings for averaging
            raw_adc_value = np.mean([ads.get_diff_channel_value(ch_pair) for _ in range(10)])
            adc_values.append(raw_adc_value)

            print(f"Weight: {weight} lbs - Averaged ADC value: {raw_adc_value:.2f}")
            
            if weight == 0:
                zero_load_offsets[channel_name] = raw_adc_value  # Save zero-load offset
        
        # Perform linear regression to get slope
        slope, *_ = linregress(adc_values, weights)
        calibration_factors[channel_name] = slope
        
    # Write calibration factors and zero load offsets to JSON
    final_data = {
        "calibration_factors": calibration_factors,
        "zero_load_offsets": zero_load_offsets
    }

    with open('calibration.json', 'w') as json_file:
        json.dump(final_data, json_file, indent=4)
    
    print("\nCalibration complete! Slopes and zero load offsets saved to 'calibration.json'.")
    return final_data
