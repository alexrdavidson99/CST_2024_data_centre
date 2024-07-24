import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy

def process_section_data(section_data, section_index):
    df = pd.DataFrame(section_data, columns=["x", "z"])
    
    # Format section name
    new_section_name = f"pixel {section_index:.1f}"
    
    return new_section_name, df

# Define file path
#file_path = "C:/Users/lexda/Downloads/paricles_sweep_500_to_1200v.txt"
file_path = "C:/Users/lexda/Downloads/42_samples_same_paramters.txt"
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
            #print(section_name)
        else:
            # Parse data lines and append to current section data
            parts = line.strip().split()
            if len(parts) >= 2:
                x = float(parts[0])
                z = float(parts[1])
                section_data.append((x, z))

    # Process the last section after end of file
    if section_data:
        new_section_name, filtered_df = process_section_data(section_data, section_index)
        data_frames.append((new_section_name, filtered_df))

# Now `data_frames` contains tuples of (new_section_name, DataFrame) for each section with filtered data


plt.figure(figsize=(10, 6))  

list = np.linspace(1, 43, 43)

numner_of_electrons = []
for section_index, (section_name, df) in enumerate(data_frames, start=1):
    print(len(df.index), list[section_index-1])
   
    
    
    #plt.hist2d(df["x"], df["z"], bins=50, label=f'pixel {list[section_index-1]}', alpha=0.5)
    #if section_index == 2 or section_index == 9:
    #    plt.scatter(df["x"], df["z"], label=f'pixel {list[section_index-1]}', alpha=0.5)
    #    plt.hist(df["z"], bins=50, label=f'{section_index}', alpha=0.5, log=True )
    
    numner_of_electrons.append(len(df.index))
plt.hist(numner_of_electrons, bins=5, alpha=0.5, log=True )
print (numner_of_electrons)
plt.title("Electron distribution in the x direction at different back gap voltages values")
plt.xlabel("position (um)")
plt.ylabel("Events")
plt.legend()
plt.savefig("C:/Users/lexda/VsProjects/CST_2024_data_center/cst_data/parameter_sweep_voltage/500_to_1200v.png")


plt.grid(True)

plt.tight_layout()
