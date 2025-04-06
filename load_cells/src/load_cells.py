# Function to convert raw ADC values (voltages) to weights
def voltage_to_weight(voltage, slope, intercept):
    return voltage * slope + intercept

# Function to convert the voltages into weights using calibration factors
def convert_voltages_to_weights(voltages, calibration_factors):
    weights_dict = {}
    for key, voltage_list in voltages.items():
        slope, intercept = calibration_factors[key]
        weights = [max(0, voltage_to_weight(voltage, slope, intercept)) for voltage in voltage_list]
        weights_dict[key] = weights
    return weights_dict

# Function to read voltages from load cells
def read_voltages(ads):
    adc_values = {f"Differential {i*2}-{i*2+1}": [] for i in range(4)}
    for ch_pair in range(4):  # Iterate over channel pairs 0-3
        ADC_Value = ads.get_diff_channel_value(ch_pair)
        adc_values[f"Differential {ch_pair*2}-{ch_pair*2+1}"].append(ADC_Value)
    return adc_values
