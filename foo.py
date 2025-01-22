from my_CST_functions import output_data_from_file

output_values = output_data_from_file("C:/Users/lexda/Downloads/number_of_hits_per_SEE_gen_track_100.txt")
first_gen = []
second_gen = []
for i in range(0, 26):
    first_output_values = output_values[i][1]
    first_gen.append(first_output_values.iloc[1, 1])
    second_gen.append(first_output_values.iloc[2, 1])
    
print(f"First generation: {first_gen}")
print(f"Second generation: {second_gen}")