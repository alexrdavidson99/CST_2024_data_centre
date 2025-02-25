import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
from my_CST_functions import output_data_from_file

# looking a the distubution of electrons in the x direction runnung nondeterministic mutiple times
# Define file path
#file_path = "C:/Users/lexda/Downloads/paricles_sweep_500_to_1200v.txt"
file_path = "C:/Users/lexda/Downloads/42_samples_same_paramters.txt"

data_frames, data_sums = output_data_from_file(file_path)
print(data_sums)


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
