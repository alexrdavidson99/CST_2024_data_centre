import pandas as pd

def process_section_data(section_data, section_index):
    df = pd.DataFrame(section_data, columns=["x", "z"])
    
    # Format section name
    new_section_name = f"pixel {section_index:.1f}"
    
    return new_section_name, df

def output_data_from_file(file_path):
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
    return data_frames