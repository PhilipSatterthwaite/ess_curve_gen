import os
import pandas as pd

def extract_output_data(directory_name: str, file_name: str = None):
    if file_name is None or file_name == "":
        script_directory = os.path.dirname(os.path.abspath(__file__))
        outputs_directory = os.path.join(script_directory, directory_name)
        files = os.listdir(outputs_directory)
        if len(files) > 0:
            file_name = files[0]
            file_path = os.path.join(outputs_directory, file_name)

            with open(file_path, 'r') as file:
                lines = file.readlines()

            data = [line.split() for line in lines]
            df = pd.DataFrame(data)
            for index, row in df.iloc[1:, :].iterrows():
                for column in df.columns:
                    value = str(row[column])  # Convert to string to access characters by index
                    if len(value) >= 4 and value[-4] == '-' and value[-3].upper() != 'E':
                        df.at[index, column] = 0
            df.iloc[1:,:] = df.iloc[1:,:].astype(float)
            #df_data = df.iloc[1:,:]
            return df
        else:
            print("Error: There is not exactly one file in the directory.")
    else:
        file_path = os.path.join(directory_name, file_name)
        with open(file_path, 'r') as file:
            lines = file.readlines()

        data = [line.split() for line in lines]
        df = pd.DataFrame(data)
        for index, row in df.iloc[1:, :].iterrows():
            for column in df.columns:
                value = str(row[column])  # Convert to string to access characters by index
                if len(value) >= 4 and value[-4] == '-' and value[-3].upper() != 'E':
                    df.at[index, column] = 0
        df.iloc[1:,:] = df.iloc[1:,:].astype(float)
        return df