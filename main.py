import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import functools
from pathlib import Path
import re
import os
import sys
from scipy import signal
from scipy.integrate import quad

# Load the data
def f(x):
    return np.interp(x, data_from_string["x"], data_from_string["y"])

def butter_lowpass_filter(data, cutoff_freq, fs, order=4):
    nyquist_freq = 0.5 * fs
    normalized_cutoff = cutoff_freq / nyquist_freq
    b, a = signal.butter(order, normalized_cutoff, btype='low')
    return signal.lfilter(b, a, data)



if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate a heatmap from a CSV file.')
    parser.add_argument('--filename', type=str, default='./cst_data/xpos_vs_ypos_js_2500um_from_pore.txt', help='Path to the CSV file')
    
    args = parser.parse_args()
    path_string = args.filename
    
    data_from_string = pd.read_csv( path_string, comment='#', names=["x", "y"], skiprows=3, sep="\t+", engine='python')
    #plt.plot(data_from_string["x"], data_from_string["y"], label="900V")
    data = data_from_string['y']
   
    
    order = 4  # Filter order
    cutoff_freq = 15 # Cutoff frequency in Hz
    fs = 2e5  # Sampling frequency in Hz
    filtered_data = butter_lowpass_filter(data, cutoff_freq, fs, order=4)

    plt.plot(data_from_string["x"], filtered_data, label="Filtered")

    low = data_from_string["x"].min()  # Lower limit
    high = data_from_string["x"].max()  # Upper limit

    # Integrate the function from a to b
    result, error = quad(f, low,high)

    print("Result of integration:", result)
    print("Estimated error:", error)

    x_curve = np.linspace(low, high, 100)
    y_curve = f(x_curve)
    plt.fill_between(data_from_string["x"], filtered_data, alpha=0.5)





    plt.show()
