from extract_output_data import extract_output_data
from name_and_save import name_and_save
from error_plot import error_plot
import os

def find_max(directory):

    ############################ needs to be generalized to work with any directory full of error data

    #max_error_df = create_empty_dataframe(directory)
    max_error_df = extract_output_data(directory).iloc[[0]]
    max_error_df.iloc[0, 0] = 'Fuel1_Frac'

    filenames = sorted(os.listdir(directory))
    for filename in filenames:
        hep_frac = float(filename[6:10])
        df = extract_output_data(directory, filename)
        subset = df.iloc[1:, 1:].astype(float)

        # Find the maximum value in each column
        max_values = subset.abs().max()
        new_row = [hep_frac] + list(max_values)
        max_error_df.loc[len(max_error_df)] = new_row

    file_name = "max_error.Y"
    name_and_save(max_error_df, file_name, directory)
    return max_error_df

#directory = "combined_error"
#max_error_df = extract_output_data("combined_error", "max_error")

#col = list(range(3, 43)) + list(range(45, 50))
#col = [3,7,10,11, 14,18]
#error_plot(max_error_df, col, "% Toluene", "Maximum Error", "Major Species") #, max_error_df.iloc[0,col[0]]

