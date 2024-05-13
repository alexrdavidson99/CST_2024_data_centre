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


font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'bold',
        'size': 16,
 
        }



if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate a plot from CSV files.')
    parser.add_argument('--filenames', nargs='+', type=str, default=['./cst_data/xpos_vs_ypos_js_2500um_from_pore.txt'], help='Paths to the CSV files')
    args = parser.parse_args()

    # Initialize plot
    plt.figure(figsize=(10, 6))

    # Loop through each filename
    for filename in args.filenames:
        data = pd.read_csv(filename, comment='#', names=["x", "y"], skiprows=3, sep="\t+", engine='python')
        plt.scatter(data["x"], data["y"], label=filename)
    
    #data_from_string = pd.read_csv( path_string, comment='#', names=["x", "y"], skiprows=3, sep="\t+", engine='python')
    #plt.plot(data_from_string["x"], data_from_string["y"], label="900V")
    #plt.hist2d(data_from_string["x"], data_from_string["y"], bins=20, label="900V")
    #data = data_from_string['y']
    #plt.plot(data_from_string["x"], data, label="Original")
    
    order = 4  # Filter order
    cutoff_freq = 15 # Cutoff frequency in Hz
    fs = 2e5  # Sampling frequency in Hz
    filtered_data = butter_lowpass_filter(data, cutoff_freq, fs, order=4)

    #plt.plot(data_from_string["x"], filtered_data, label="Filtered")

    #low = data_from_string["x"].min()  # Lower limit
    #high = data_from_string["x"].max()  # Upper limit

    # Integrate the function from a to b
    #result, error = quad(f, low,high)

    #print("Result of integration:", result)
    #print("Estimated error:", error)

    #x_curve = np.linspace(low, high, 100)
    #y_curve = f(x_curve)
    #plt.fill_between(data_from_string["x"], filtered_data, alpha=0.5)




    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("x vs y")
    plt.text(1000, 1500, r'1300 v 500 ', fontdict=font)
    plt.legend()
    plt.show()
