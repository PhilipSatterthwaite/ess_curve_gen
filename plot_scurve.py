import os
from radrun import run_radcase
from average_outputs import avg_data
from combined_output import run_combined_case
from calc_error import error_calc
from error_plot import error_plot
from extract_output_data import extract_output_data
import matplotlib.pyplot as plt
import pandas as pd
from name_and_save import name_and_save
import numpy as np
from find_max import find_max
from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt

rmin = 0.1
rmax = 50
n = 10
chis = []
max_temps = []
directory = "rad_var"

for file_name in sorted(os.listdir(directory)):  # Sorting ensures files are processed in order
    if file_name.endswith(".Y"):  # Process only relevant files
        try:
            chi = float(file_name[3:-2])  # Extracting radius from filename (e.g., "rad12.34.Y")
        except ValueError:
            continue  # Skip files that don't match the expected format

        df = extract_output_data("", os.path.join(directory, file_name))
    df = extract_output_data("rad_var", file_name)
    temps = df.iloc[1:, 2]
    max_temp = max(temps)
    
    # Store values for plotting
    chis.append(1/chi)
    max_temps.append(max_temp)

# Plotting
plt.scatter(chis, max_temps, color='b', label='Max Temperature')
plt.xlabel("1/Chi")
plt.ylabel("Max Temperature")
plt.title("Max Temperature vs. Radius")
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(8, 6))

for file_name in sorted(os.listdir(directory)):  
    if file_name.endswith(".Y"):  
        try:
            chi = float(file_name[3:-2])  
        except ValueError:
            continue  

        df = extract_output_data("", os.path.join(directory, file_name))
        col1 = df.iloc[1:, 0]  # Column 1
        col2 = df.iloc[1:, 46]  # Column 2

        # Plot each dataset with a label
        plt.plot(col1, col2, label=f"Chi ref {chi:.2f}")

# Customize and show the second plot
plt.xlabel("Z")
plt.ylabel("SDR")
plt.legend()
plt.grid(True)
plt.show()
