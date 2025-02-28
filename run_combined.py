from average_outputs import avg_data
from combined_output import run_combined_case
from calc_error import error_calc
from error_plot import error_plot
from extract_output_data import extract_output_data
from find_max import find_max

n = 100
for i in range(n+1):
    hep_frac = (n-i)/n
    tol_frac = i/n

    average = avg_data(hep_frac, "z_hep_data.Y", "z_tol_data.Y")
    for index, row in average.iloc[1:, :].iterrows():
        for column in average.columns:
            value = str(row[column])  # Convert to string to access characters by index
            if len(value) >= 4 and value[-4] == '-' and value[-3].upper() != 'E':
                average.at[index, column] = 0
                
    combined = run_combined_case(hep_frac, tol_frac, "input_base_combined")
    #combined_name = f"{hep_frac}hep_{tol_frac}tol.Y"
    #combined = extract_output_data("combined", combined_name)
    
    
    error_name = f"error_{hep_frac:.2f}hep_{tol_frac:.2f}tol.Y"
    error = error_calc(combined, average, error_name, "combined_error")

directory = "combined_error"
max_error_df=find_max(directory)

col = list(range(3, 50))
error_plot(max_error_df, col, "% Toluene", "Maximum Error", "All Error") #, max_error_df.iloc[0,col[0]]