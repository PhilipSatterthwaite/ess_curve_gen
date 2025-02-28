import pandas as pd

def avg_data(fuel1_frac: float, fuel1_filename: str, fuel2_filename: str):
    """
    Calculate the weighted average of two data sets.

    Inputs:
    - fuel1_frac: percent weight of fuel1 results
    - fuel1_filename: filename for fuel1 data
    - fuel2_frac: percent weight of fuel2 results
    - fuel2_filename: filename for fuel2 data

    Output:
    - data structure of properly weighted average between the two input files

    Raises:
    - ValueError if the two data sets are not the same size
    - ValueError if the first row of the two data sets do not match exactly
    - ValueError if the first column of the two data sets do not match exactly
    """
    
    fuel2_frac = 1-fuel1_frac

    with open(fuel1_filename, 'r') as file:
        lines = file.readlines()

    data = [line.split() for line in lines]
    df_fuel1 = pd.DataFrame(data)
    fuel1_data = df_fuel1.iloc[1:,:]

    with open(fuel2_filename, 'r') as file:
        lines = file.readlines()

    data = [line.split() for line in lines]
    df_fuel2 = pd.DataFrame(data)
    fuel2_data = df_fuel2.iloc[1:,:]

    if fuel1_data.shape != fuel2_data.shape:
        raise ValueError("The two data sets are not the same size.")
    
    if not df_fuel1.iloc[0].equals(df_fuel2.iloc[0]):
        raise ValueError("Variable names for two data sets are not the same.")

    if max(abs(fuel1_data.iloc[1:, 0].astype(float) - fuel2_data.iloc[1:, 0].astype(float))) > 0:
        raise ValueError("Mixture fraction Z (first column) is not the same for both sets.")

    average = fuel1_data.apply(lambda x: x.astype(float) * fuel1_frac) + fuel2_data.apply(lambda x: x.astype(float) * fuel2_frac)

    column_titles = df_fuel1.iloc[0, :]
    average_with_titles = pd.concat([column_titles.to_frame().T, average], ignore_index=True)
    return average_with_titles