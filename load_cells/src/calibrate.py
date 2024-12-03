import ADS1256
import time
import os

# def calibrate();
# # Initialize ADC
# ADC = ADS1256.ADS1256()
# if ADC.ADS1256_init() == -1:
#     exit()

# # Calibration data
# weights = [0, 5, 10, 25, 50]  # Example weights in grams

# # Check if the file already exists
# file_exists = os.path.isfile('calibration_data3.csv')

# # Open a file to save or append the calibration data
# with open('calibration_data3.csv', 'a') as file:  # 'a' opens the file in append mode
#     # Write the header row if the file is new
#     if not file_exists:
#         file.write("Weight (pounds),ADC Value\n")

#     print("Place each weight on the load cell and press Enter to record its value.")
#     for weight in weights:
#         input("Place {} pounds on the load cell. Then press Enter...".format(weight))
#         raw_adc = ADC.ADS1256_GetDiffChannalValue()
#         print("Recorded value for {} pounds: {}".format(weight, raw_adc))
        
#         # Append the weight and raw ADC value to the file
#         file.write("{},{}\n".format(weight, raw_adc))

#         time.sleep(1)  # Short delay to stabilize

# print("Calibration data saved to 'calibration_data3.csv'.")




##### Here is the calibrationcurve.py code:


# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import linregress

# # Load the calibration data from CSV
# data = pd.read_csv('calibration_data1.csv')

# # Perform linear regression
# slope, intercept, r_value, p_value, std_err = linregress(data['ADC Value'], data['Weight (pounds)'])

# # Function to convert raw ADC value to weight
# def adc_to_weight(adc_value):
#     return (adc_value * slope) + intercept

# # Display the calibration equation and R-squared value
# print(f"Calibration Equation: weight = ({slope} * ADC Value) + {intercept}")
# print(f"R-squared: {r_value**2}")

# # Plotting the calibration curve
# plt.figure(figsize=(10, 6))
# plt.scatter(data['ADC Value'], data['Weight (pounds)'], color='blue', label='Calibration Data')
# plt.plot(data['ADC Value'], slope * data['ADC Value'] + intercept, color='red', label='Fitted Line')

# plt.title('Load Cell Calibration Curve')
# plt.xlabel('ADC Value')
# plt.ylabel('Weight (pounds)')
# plt.legend()
# plt.grid(True)
# plt.show()

# # Example conversion
# example_adc_value = 7500
# converted_weight = adc_to_weight(example_adc_value)
# print(f"The weight for ADC value {example_adc_value} is approximately {converted_weight:.2f} pounds.")