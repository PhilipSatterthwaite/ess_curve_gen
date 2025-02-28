from extract_output_data import extract_output_data
from name_and_save import name_and_save

#sets zeros where values are less than E-100
def set_zeros(directory_name: str, file_name: str = None):
    df = extract_output_data(directory_name, file_name)
    for index, row in df.iloc[1:, :].iterrows():
        for column in df.columns:
            value = str(row[column])  # Convert to string to access characters by index
            if len(value) >= 4 and value[-4] == '-' and value[-3].upper() != 'E':
                df.at[index, column] = 0
    df.iloc[1:, :] = df.iloc[1:, :].astype(float)
    name_and_save(df,file_name,directory_name)