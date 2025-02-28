import os
from staged_output import run_staged_case
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
#staged = run_staged_case()



#for i in range(11):
#    hep_frac = (10-i)/10
#    tol_frac = i/10
    #run_case(hep_frac, tol_frac)



H_hep = 16
C_hep = 7
H_tol = 8
C_tol = 7

HC_hep = H_hep/C_hep
HC_tol = H_tol/C_tol
FO_hep_stoic = 1/11
FO_tol_stoic = 1/9

dataframe_base = extract_output_data('', 'z_hep_data.Y')
dataframe_base.iloc[2:-1, 1:] = 0

# only include NER <= 0.5
for index, row in dataframe_base.iloc[1:][::-1].iterrows():
    first_element = float(row.iloc[0])
    if first_element > 0.5:
        dataframe_base.drop(index, inplace=True)

n = 50
#for i in range(0,n):
for i in range(0,n+1):
    fuel1_frac = (n-i)/(2*n) #molar concentration of fuel 1
    file_name = f"{fuel1_frac:.2f}hep_{1-fuel1_frac:.2f}tol.Y"
    if os.path.exists(os.path.join("staged", file_name)):
        continue
    #fuel1_frac = 0.4
    print(f"Fuel Fraction: {fuel1_frac}")
    df = dataframe_base
    NERs = np.zeros_like(dataframe_base.iloc[1:,1])
    def run_iteration(j):

        NER_total = float(df.iloc[j,0]) #total mixture NER
        #print(f"NER:{NER_total}")

        # assume total moles of stoich fuel is 1. Leave O2 constant moles. Find new real phi values
        F_hep_stoic = fuel1_frac
        F_tol_stoic = 1-fuel1_frac
        O_tot = F_hep_stoic/FO_hep_stoic + F_tol_stoic/FO_tol_stoic

        phi_tot = NER_total/(1 - NER_total + 1e-8)

        F_hep = phi_tot * fuel1_frac
        F_tol = phi_tot * (1 - fuel1_frac)

        phi_first = (F_hep/O_tot)/FO_hep_stoic
        NER_first = phi_first/(1 + phi_first)

        H_total = H_hep * F_hep + H_tol * F_tol
        C_total = C_hep * F_hep + C_tol * F_tol
        HC_total = H_total/C_total

        Z_sample = (HC_total - HC_hep) / (HC_tol - HC_hep)

        NER_sample = NER_total
        #Heptane is first fuel, toluene is second fuel
        row = run_staged_case('z_hep_data.Y', 'input_base_staged', NER_first, NER_sample, fuel1_frac)
        
        NERs[j-1] = NER_first
        return row.iloc[1:]
    # Run the iterations in parallel
    
    #parallelizing stuff
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_iteration, j) for j in range(2, len(df))]
        results = [f.result() for f in futures]

    for j in range(2,len(df)):
        df.iloc[j,1:] = results[j-2]
    #for i in range(2,len(df)):
    #    run_iteration(i)
    combined_name = f"{fuel1_frac:.2f}hep_{1-fuel1_frac:.2f}tol.Y"
    combined = extract_output_data("combined", combined_name)
    for index, row in combined.iloc[1:][::-1].iterrows():
        first_element = float(row.iloc[0])
        if first_element > 0.5:
            combined.drop(index, inplace=True)
    # make terms that are less than E-100 equal 0
    for index, row in df.iloc[1:, :].iterrows():
        for column in df.columns:
            value = str(row[column])  # Convert to string to access characters by index
            if len(value) >= 4 and value[-4] == '-' and value[-3].upper() != 'E':
                df.at[index, column] = 0

    df.iloc[1:, :] = df.iloc[1:, :].astype(float)
    name_and_save(df, file_name, "staged")

    error_name = f"error_{fuel1_frac:.2f}hep_{1-fuel1_frac:.2f}tol.Y"
    error = error_calc(combined, df, error_name, "staged_error")
    


#-------------------------------------------------
directory = "staged_error"
max_error_df=find_max(directory)
col = [3,7,10,11,14,18]
error_plot(max_error_df, col, "Heptane Fraction", "Maximum Error", "Major Species", True) #, max_error_df.iloc[0,col[0]]









'''
# ------------------------------------------------
col = [3,7,10,11,14,18]

#error_df = extract_output_data("staged", file_name)
#error_vals = error_df.iloc[1:, :]
#for i in range(len(col)):
#    plt.plot(error_vals.iloc[:,0].astype(float), error_vals.iloc[:,col[i]].astype(float), label=error_df.iloc[0, col[i]])
plt.plot(df.iloc[1:,0].astype(float), NERs, label = 'NER First')
# Add labels and title
plt.xlabel('Total NER')
plt.ylabel('First NER')
plt.title('50/50 Mixture')
plt.legend()

# Show plot
plt.show()
'''