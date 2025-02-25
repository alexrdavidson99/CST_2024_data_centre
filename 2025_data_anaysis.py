import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np 
from pathlib import Path


def open_CSV_studio_txt_data(file_path):
    with open(file_path, "r") as file:
        sections = re.split(r"#Parameters\s*=\s*{", file.read())[1:]  # Split by parameter blocks

    data_sections = []
    for sec in sections:
        param_part, *data_part = sec.split("\n#", 1)  # Split parameters from data
        params = dict(re.findall(r"(\w+)=([\d.-]+)", param_part))  # Extract key-value pairs
        
        data_lines = [line for line in data_part[0].split("\n") if line and not line.startswith("#")]
        rows = [line.split("\t") for line in data_lines]
        
        df = pd.DataFrame(rows[1:], columns=rows[0]).apply(pd.to_numeric, errors="ignore")
        data_sections.append((params, df))

    return data_sections



#file_path = "C:/Users/lexda/Downloads/sweep_3_17_step_2_deg_float_para_res_height.txt"
#file_path = "C:/Users/lexda/Downloads/number_of_particles_time_5_2D_cuts_with_SEY_set_to_4_500ev.txt"
file_path =Path("C:/Users/lexda/local_pmt_info/CST_data/gain_monitor_2/")
plot_files = list(file_path.glob("*.txt"))
# Read file and split sections
for i, plot_file  in enumerate(plot_files):
    totals = []
    angles = []
    positions_of_2d_cut = []
    # Display first dataset
    #v = next((i for i, part in enumerate(plot_file.stem.split("_")) if part.endswith('ev')), None)
    #ev = plot_file.stem.split("_")[v]
    #print(f"ev: {ev}")

    
    data_sections = open_CSV_studio_txt_data(plot_file)
    for i in range(len(data_sections)):
        params, df = data_sections[i]
        
        angle = int(params.get('mcp_angle'))
        res_height = float(params.get('res_height'))
        cut_2d = (res_height/5)*i 
        
        second_column = df.iloc[:, 1]
        total = sum(second_column)
        angles.append(angle)
        positions_of_2d_cut.append(cut_2d)
        totals.append(total)
        
        

    angles = np.array(angles)
    totals = np.array(totals)
    sorted_indices = np.argsort(angles)
    angles = angles[sorted_indices]
    totals = totals[sorted_indices]


    plt.scatter(angles,totals, label=f"peak ev from SEY curve: ")
    #plt.plot(positions_of_2d_cut,totals)
    plt.xlabel("MCP angle")
    plt.xlabel("location in pore [um]")
    plt.yscale("log")
    plt.ylabel("number of electrons per 2d cut")
plt.legend()
plt.show()