import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

def gaus(x, a, x0, sigma):
    '''
     1D gaussian
    '''
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))




# Path to the CSV file
#file_path = 'C:/Users/lexda/Downloads/ascii_export_one_pore.csv'
#file_path = 'C:/Users/lexda/Downloads/ascii_export_1000v.csv'
#file_path = 'C:/Users/lexda/Downloads/voltage_v_time_80,000_electrons_pad_2_2_e_11_ts_solver.txt'

# Initialize variables
frame_events = {}
current_frame = None
event_count = 0
total_events = 0 

# Read the CSV file
with open(file_path, mode='r') as file:
    reader = csv.reader(file)
    
    for row in reader:
        # Flatten the row to a single string
        line = ' '.join(row).strip()
        
        if line.startswith('# Frame'):
            if current_frame is not None:
                frame_events[current_frame] = event_count
            current_frame = int(line.split()[2])/ 50 # Convert to ns by dividing by 100 be
            event_count = 0
        elif line and not line.startswith('#'):
            event_count += 1
            total_events += 1

    # Add the last frame
    if current_frame is not None:
        frame_events[current_frame] = event_count


print(f'Total events: {total_events}')

#popt, pcov = curve_fit(gaus, list(frame_events.keys()), list(frame_events.values()), p0=[1, 0, 1])
#x_gauss = np.linspace(0, 0.7, 2000)
#y_gauss = gaus(x_gauss, *popt)


#FWHM = -2.355 * popt[2]
#print(f'FWHM: {FWHM}')
print (frame_events)
plt.scatter(list(frame_events.keys()), list(frame_events.values()))
#plt.plot(x_gauss, y_gauss, label=f'Gaussian fit: FWHM = {FWHM:.2f} ns')
plt.xlabel('ns')
plt.ylabel('Event count')
plt.title('Time vs Event count')
plt.legend()
plt.show()
