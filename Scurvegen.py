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

rmin = 1e-5
rmax = 1e-2
n = 10
for i in range(0,n+1):
    radius = (rmax-rmin)/n*i + rmin
    file_name = f"rad{radius:.2f}.Y"
    if os.path.exists(os.path.join("rad_var", file_name)):
        continue

    print(f"Radius: {radius}")
    df = run_radcase('input_dryer_base', radius)

    # make terms that are less than E-100 equal 0
    for index, row in df.iloc[1:, :].iterrows():
        for column in df.columns:
            value = str(row[column])  # Convert to string to access characters by index
            if len(value) >= 4 and value[-4] == '-' and value[-3].upper() != 'E':
                df.at[index, column] = 0
    name_and_save(df, file_name, "rad_var")

