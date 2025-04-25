# Function to convert raw ADC values to weights
def adc_to_weight(adc_value, slope, zero_offset):
    corrected_adc = adc_value - zero_offset
    return slope * corrected_adc

# Function to convert the ADC values into weights using calibration factors
def convert_adc_to_weights(adc_values, calibration_factors, zero_load_offsets):
    weights_dict = {}
    for key, adc_list in adc_values.items():
        slope = calibration_factors[key]
        zero_offset = zero_load_offsets[key]
        weights = [max(0, adc_to_weight(adc, slope, zero_offset)) for adc in adc_list]
        weights_dict[key] = weights
    return weights_dict

# Function to read ADC values from load cells
def read_adc_values(ads):
    adc_values = {f"Differential {i*2}-{i*2+1}": [] for i in range(4)}
    for ch_pair in range(4):  # Iterate over channel pairs 0-3
        adc_value = ads.get_diff_channel_value(ch_pair)
        adc_values[f"Differential {ch_pair*2}-{ch_pair*2+1}"].append(adc_value)
    return adc_values
