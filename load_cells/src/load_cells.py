import time
import pandas as pd
from src.ADS1256 import ADS1256

# Function to convert raw ADC values (voltages) to weights
def voltage_to_weight(voltage, slope, intercept):
    return voltage * slope + intercept

# Function to convert the voltages into weights using calibration factors
def convert_voltages_to_weights(voltages, calibration_factors):
    weights_dict = {}
    for key, voltage_list in voltages.items():
        slope, intercept = calibration_factors[key]
        weights = [voltage_to_weight(voltage, slope, intercept) for voltage in voltage_list]
        weights_dict[key] = weights
    return weights_dict

# Function to read voltages from load cells
def read_voltages(ads):
    duration = 3  # Duration in seconds

    adc_values = {f"Differential {i*2}-{i*2+1}": [] for i in range(4)}
    start_time = time.time()

    # Read voltage values for the specified duration
    while time.time() - start_time < duration:
        for ch_pair in range(4):  # Iterate over channel pairs 0-3
            ADC_Value = ads.ADS1256_GetDiffChannalValue(ch_pair)
            adc_values[f"Differential {ch_pair*2}-{ch_pair*2+1}"].append(ADC_Value)
    
    return adc_values
