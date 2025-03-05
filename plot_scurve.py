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
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.collections import LineCollection


chis = []
max_temps = []
directory = "chi_var_new"

for file_name in sorted(os.listdir(directory)):  # Sorting ensures files are processed in order
    if file_name.endswith(".Y"):  # Process only relevant files
        try:
            chi = float(file_name[3:-2])  # Extracting radius from filename (e.g., "rad12.34.Y")
        except ValueError:
            continue  # Skip files that don't match the expected format

        df = extract_output_data("", os.path.join(directory, file_name))
    df = extract_output_data(directory, file_name)
    temps = df.iloc[1:, 2]
    max_temp = max(temps)
    
    # Store values for plotting
    chis.append(1/chi)
    max_temps.append(max_temp)

chis_trunc = []
max_temps_trunc = []
directory_trunc = "chi_var_trunc"

for file_name in sorted(os.listdir(directory_trunc)):  # Sorting ensures files are processed in order
    if file_name.endswith(".Y"):  # Process only relevant files
        try:
            chi = float(file_name[3:-2])  # Extracting radius from filename (e.g., "rad12.34.Y")
        except ValueError:
            continue  # Skip files that don't match the expected format

        df = extract_output_data("", os.path.join(directory, file_name))
    df = extract_output_data(directory, file_name)
    temps = df.iloc[1:, 2]
    max_temp = max(temps)
    
    # Store values for plotting
    chis_trunc.append(1/chi)
    max_temps_trunc.append(max_temp)

# Plotting
plt.scatter(chis, max_temps, color='b', label='Max Temperature')
plt.scatter(chis_trunc, max_temps_trunc, color='g', label='Max Temperature')
plt.xlabel(r"$1/\chi $ [s]")
plt.ylabel(r"$T_{max} $ [K]")
plt.legend()
plt.grid(True)
plt.show()


directory = "chi_var_new"
chis = []
lines = []
colors = []

plt.figure(figsize=(8, 6))

# Collect all chi values for normalization
for file_name in sorted(os.listdir(directory)):  
    if file_name.endswith(".Y"):  
        try:
            chi = float(file_name[3:-2])  
            chis.append(chi)
        except ValueError:
            continue  

# Normalize chi values for colormap
norm = mcolors.Normalize(vmin=min(chis), vmax=max(chis))
cmap = cm.coolwarm  # Choose a colormap

# Prepare line segments for LineCollection
for file_name in sorted(os.listdir(directory)):  
    if file_name.endswith(".Y"):  
        try:
            chi = float(file_name[3:-2])  
        except ValueError:
            continue  

        df = extract_output_data("", os.path.join(directory, file_name))
        col1 = df.iloc[1:, 0].values  # Column 1 (Z)
        col2 = df.iloc[1:, 2].values  # Column 2 (SDR)

        # Create line segments
        segments = [np.column_stack([col1, col2])]
        lines.extend(segments)
        colors.append(cmap(norm(chi)))  # Assign color based on chi

# Create a LineCollection
lc = LineCollection(lines, colors=colors, linewidth=2)

# Add to plot
ax = plt.gca()
ax.add_collection(lc)

# Adjust limits
ax.autoscale()
plt.xlabel("Z")
plt.ylabel("T [K]")
plt.grid(True)

# Add color bar
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label("Reference SDR")

# Show the plot
plt.show()