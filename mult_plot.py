import pandas as pd
import matplotlib.pyplot as plt


def process_section_data(section_data, section_index):
    df = pd.DataFrame(section_data, columns=["Time (ns)", "Value"])
    df.set_index('Time (ns)', inplace=True)
    data = df["Value"]
    #filtered_data = butter_lowpass_filter(data, order=4)
   
    # Create DataFrame for filtered data
    filtered_df = pd.DataFrame({"Value": data}, index=df.index)
    
    # Format section name
    new_section_name = f"pixel {section_index:.1f}"
    
    return new_section_name, filtered_df

# Define file path
file_path = "C:/Users/lexda/Downloads/SEY_3.5_to_3.8_x_v_z.txt"

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
                time_ns = float(parts[0])
                value = float(parts[1])
                section_data.append((time_ns, value))

    # Process the last section after end of file
    if section_data:
        new_section_name, filtered_df = process_section_data(section_data, section_index)
        data_frames.append((new_section_name, filtered_df))

# Now `data_frames` contains tuples of (new_section_name, DataFrame) for each section with filtered data


plt.figure(figsize=(10, 6))  
list = [1, 2, 3, 4, 5]
SEY= [3.5, 3.6, 3.7, 3.8]
numner_of_electrons = []
for section_index, (section_name, df) in enumerate(data_frames, start=1):
    print(len(df.index), list[section_index-1])
    #plt.plot(list[section_index-1],len(df.index), label=f'SEY={(section_index/10)3.5}')
    #plt.hist(df["Value"], bins=50, label=f'SEY={-((section_index/10)-3.9):.1f}', alpha=0.5, log=True )
    #plt.scatter(df.index, df["Value"], label=f'01({section_index})', alpha=0.5 )
    
    numner_of_electrons.append(len(df.index))

print(reversed(list[1:5]))
plt.plot(SEY, numner_of_electrons,  label="Electrons")
plt.yscale('log')
# Customize x-axis to display time in datetime format
plt.title("Power vs Time for 5 pixels")
plt.xlabel("position (um)")
plt.ylabel("Events")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

