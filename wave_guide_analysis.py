import pandas as pd
from scipy import signal

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks


from scipy.optimize import curve_fit



def gaussian(x, A, mu, sigma):
    return A * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def butter_lowpass_filter(data, order=4):
    cutoff_freq = 5  # Cutoff frequency in Hz
    fs = 10000  # Sampling frequency in Hz
    nyquist_freq = 0.5 * fs
    normalized_cutoff = cutoff_freq / nyquist_freq
    b, a = signal.butter(order, normalized_cutoff, btype='low')
    return signal.lfilter(b, a, data)





def process_section_data(section_data, section_index):
    df = pd.DataFrame(section_data, columns=["Time (ns)", "Value"])
    df.set_index('Time (ns)', inplace=True)
    data = df["Value"]
    filtered_data = butter_lowpass_filter(data, order=4)
    #filtered_data = data
   
    # Create DataFrame for filtered data
    filtered_df = pd.DataFrame({"Value": filtered_data}, index=df.index)
    
    # Format section name
    new_section_name = f"pixel {section_index:.1f}"
    
    return new_section_name, filtered_df

# Define file path
#file_path = "C:/Users/lexda/Downloads/4_nodes_0.7ns.txt"
#file_path = "C:/Users/lexda/VsProjects/CST_2024_data_center/cst_data/parameter_sweep_voltage/signal_v_time_5_pixels.txt"
file_path = 'C:/Users/lexda/Downloads/voltage_v_time_80,000_electrons_pad_2_2_e_11_ts_solver.txt'
# Initialize a list to store data frames for each section
data_frames = []

# Open the file and read data section by section
with open(file_path, 'r') as file:
    section_data = []  # To accumulate data for the current section
    section_index = 1

    for line in file:
        if line.startswith('#'):  # Check for section headers
            if section_data:  # If there's accumulated data, process it
                new_section_name, filtered_df = process_section_data(section_data, section_index)
                data_frames.append((new_section_name, filtered_df))
                section_data = []  # Reset for the next section
                section_index += 1
            
            # Extract section name from comment line
            section_name = line.strip().replace('#', '', 1).strip()
            print(section_name)
        else:
            # Parse data lines and append to current section data
            parts = line.strip().split()
            if len(parts) >= 2:
                time_ns = float(parts[0])
                value = float(parts[1])
                section_data.append((time_ns, value))

    # Process the last section after end of file
    if section_data:
        new_section_name, filtered_df = process_section_data(section_data, section_index)
        data_frames.append((new_section_name, filtered_df))

# Now `data_frames` contains tuples of (new_section_name, DataFrame) for each section with filtered data


plt.figure(figsize=(10, 6))  
for section_index, (section_name, df) in enumerate(data_frames, start=1):
    plt.plot(df.index, df["Value"], label=f'01({section_index})')


file_path = 'C:/Users/lexda/Downloads/voltage_v_time_80,000_electrons_pad_2_2_e_11_ts_solver.txt'
data_from_v = pd.read_csv(file_path, delimiter='\t', names=['Time', 'Value'], skiprows=5)
time = data_from_v['Time']
voltage = data_from_v['Value']
voltage = butter_lowpass_filter(voltage, order=4)

peaks, _ = find_peaks(voltage, height=0.0006)
print (f"Peaks: {peaks}")
peak_time = time[peaks]
print (f"Peak time: {peak_time}")
peak_positions = voltage[peaks]
print (f"Peak voltage: {peak_positions}")

max_peak_pos = 0.000964
print (f"Max peak position: {max_peak_pos}")

# Extract the subset of data for fitting
fit_time = time
fit_voltage = voltage
A_guess = np.max(fit_voltage)
mu_guess = 0.326024
sigma_guess = np.std(fit_time)
popt, _ = curve_fit(gaussian, fit_time, fit_voltage, p0=[A_guess, mu_guess, sigma_guess])
A, mu, sigma = popt
sigma_s = sigma * 1e-9
# Calculate the area under the Gaussian
area = (A * sigma_s * np.sqrt(2 * np.pi))/(50*1.6e-19)
print(f" Area under the Gaussian: {area}")

#plt.plot(fit_time, fit_voltage, 'x', label='Selected Data for Fitting')

x_fit = np.linspace(min(fit_time), max(fit_time), 1000)
y_fit = gaussian(x_fit, *popt)

plt.fill_between(x_fit, y_fit, alpha=0.5, color='orange', label='Area under Gaussian')

# Customize x-axis to display time in datetime format
plt.title("Voltage vs. Time")
plt.xlabel("Time")
plt.ylabel("power^1/2 (watts)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
