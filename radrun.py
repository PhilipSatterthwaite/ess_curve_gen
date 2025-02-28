import os
import subprocess
import shutil
import pandas as pd

from average_outputs import avg_data
from calc_error import error_calc
from error_plot import error_plot
from extract_output_data import extract_output_data

def name_and_save(directory, name, destination):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                # Rename the file
                new_file_path = os.path.join(directory, name)  # New file path with the desired name
                os.rename(file_path, new_file_path)

                # Move the renamed file to the destination directory
                shutil.move(new_file_path, destination)

        except Exception as e:
            print(f"Error renaming/moving {file_path}: {e}")


def delete_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)  # Deletes the file

        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def create_products_list(file_path, NER):
    file = extract_output_data('',file_path)
    for i in range(1,len(file)):
        if file.iloc[i,0] > NER:
            break
    interp_row = file.iloc[i,:] + (NER - file.iloc[i,0]) / (file.iloc[i + 1,0] - file.iloc[i,0]) * (file.iloc[i + 1,:] - file.iloc[i,:])
    row = [(title, column) for title, column in zip(file.iloc[0,:], interp_row)]
    return row[2], row[3:-5]

def extract_closest_Z(df, Z_value):
    z_column_floats = df.iloc[1:, 0].astype(float)
    closest_index = (z_column_floats - Z_value).abs().idxmin()
    closest_row = df.iloc[closest_index][:]
    return closest_row

def extract_closest_NER(df, NER_value):
    NER_column_floats = df.iloc[1:, 0].astype(float)
    closest_index = (NER_column_floats - NER_value).abs().idxmin()
    closest_row = df.iloc[closest_index][:]
    return closest_row

  
def run_radcase(input_filename: str, radius: float):
    """
    Inputs:
    - prod_frac: percentage of products in second case
    - prod_filename: name of baseline input file
    - input_filename: name of second fuel baseline input file
    - phi_val: NEQ to find from input file
    - Z_val: output Z value to extract
    """
    
    output_directory = f"{radius}"
    script_path = os.path.dirname(os.path.abspath(__file__))
    outputs_path = os.path.join(script_path, f"outputs/{output_directory}")
    os.makedirs(outputs_path)

    # Create a temporary file
    temp_filename = f"temp_file_{output_directory}"
    #extract stoichiometric products
    try:
        # Create a copy of the input file
        if not os.path.exists(input_filename):
            raise FileNotFoundError(f"Input file '{input_filename}' not found.")
        shutil.copy(input_filename, temp_filename)
        
        # Modify the content of the new file
        with open(temp_filename, 'r') as input_file:
            lines = input_file.readlines()

        # Open the file in 'w' mode to overwrite it
        with open(temp_filename, 'w') as output_file:
            for i, line in enumerate(lines, 1):
                if i == 19:
                    edited_line = f"{line.rstrip()}     {radius}\n"
                else:
                    edited_line = line
                output_file.write(edited_line)
                
        
        print("running pdrs")
        # Run the command and capture the output
        command = f"pdrs {temp_filename}"

        try:
            # Use Popen to capture real-time output
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Read stdout and stderr line by line
            for line in process.stdout:
                print(line, end="")  # Print each line in real time

            for line in process.stderr:
                print(line, end="")  # Print error messages in real time

            # Ensure the process completes
            process.wait()

            # Check for errors
            if process.returncode != 0:
                print(f"Command failed with return code {process.returncode}")

        except Exception as e:
            print(f"Error executing command: {e}")


        # Extract combined data from file
        
        data = extract_output_data(f"outputs/{output_directory}")


    finally:
        
        # Delete the temporary file
        os.remove(temp_filename)        

        #delete_files_in_directory(outputs_directory)
        shutil.rmtree(outputs_path)
        return data