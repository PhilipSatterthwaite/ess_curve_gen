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

chi_min =-1.0
chi_max = 1.0
inv_chimin = 1/chi_max
inv_chimax = 1/chi_min
n = 30
directory = "mdot_mult_factor"
for i in range(0,n+1):
    chi = round(1/((inv_chimax-inv_chimin)/n*i + inv_chimin),2)
    chi = round(((chi_max-chi_min)*i/n + chi_min),2)
    file_name = f"chi{chi:.2f}.Y"
    if os.path.exists(os.path.join(directory, file_name)):
        continue

    print(f"Chi ref: {chi}", flush=True)
    df = run_radcase('input_dryer_base_drop', chi)

    # make terms that are less than E-100 equal 0
    for index, row in df.iloc[1:, :].iterrows():
        for column in df.columns:
            value = str(row[column])  # Convert to string to access characters by index
            if len(value) >= 4 and value[-4] == '-' and value[-3].upper() != 'E':
                df.at[index, column] = 0
    name_and_save(df, file_name, directory)

