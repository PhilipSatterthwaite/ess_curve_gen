import os
import subprocess
import shutil
import pandas as pd

from average_outputs import avg_data
from calc_error import error_calc
from error_plot import error_plot
from extract_output_data import extract_output_data
from name_and_save import name_and_save

def delete_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)  # Deletes the file

        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


def gen_name(f1_frac, f2_frac, f1_name, f2_name):
    return f"{f1_frac:.2f}{f1_name}_{f2_frac:.2f}{f2_name}.Y"



def run_combined_case(fuel1_frac: float, fuel2_frac: float, input_filename: str):
    # Create a temporary file
    temp_filename = "temp_file"
    
    try:
        # Create a copy of the input file
        shutil.copy(input_filename, temp_filename)

        # Modify the content of the new file
        with open(temp_filename, 'r') as input_file:
            lines = input_file.readlines()

        with open(temp_filename, 'w') as output_file:
            for i, line in enumerate(lines, 1):
                if i == 13:  # Add heptane_percent to the end of line 13
                    edited_line = f"{line.rstrip()} {fuel1_frac}\n"
                elif i == 14:  # Add toluene_percent to the end of line 14
                    edited_line = f"{line.rstrip()} {fuel2_frac}\n"
                else:
                    edited_line = line
                output_file.write(edited_line)

        # Run the command and capture the output
        command = f"pdrs {temp_filename}"
        try:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        except subprocess.CalledProcessError as e:
            # Handle errors (if any)
            print("Error executing command:")
            print(e.stderr)

        # Extract combined data from file
        combined = extract_output_data("outputs")

            # make terms that are less than E-100 equal 0
        for index, row in combined.iloc[1:, :].iterrows():
            for column in combined.columns:
                value = str(row[column])  # Convert to string to access characters by index
                if len(value) >= 4 and value[-4] == '-' and value[-3].upper() != 'E':
                    combined.at[index, column] = 0

    finally:
        # Delete the temporary file
        os.remove(temp_filename)
        

        #save and organize files
        script_directory = os.path.dirname(os.path.abspath(__file__))
        outputs_directory = os.path.join(script_directory, "outputs")
        
        combined_directory = os.path.join(script_directory, "combined")

        file_name = gen_name(fuel1_frac, fuel2_frac, "hep", "tol")
        name_and_save(combined, file_name, combined_directory)
        delete_files_in_directory(outputs_directory)
        print(f"{file_name} run has completed.")
    return combined