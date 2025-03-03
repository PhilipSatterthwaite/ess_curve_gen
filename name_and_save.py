import pandas as pd
import os

def scientific_notation(x):
    # Custom formatting for scientific notation with zero exponent
    if abs(x) < 1e-99:  # Change threshold as needed
        return "{:.0f}".format(x)
    else:
        return "{:0.15E}".format(x).replace('e', 'E')

def name_and_save(data, name, directory):

    data.iloc[1:,:] = data.iloc[1:,:].astype(float)
    if not os.path.exists(directory) and directory != "":
        os.makedirs(directory)
    filepath = os.path.join(directory, name)
    
    # Extract headers from the first row
    headers = data.iloc[0].tolist()   
    
    #formatted_data = pd.concat([data.iloc[1:,0], data.iloc[1:, 1:].applymap(scientific_notation)], axis=1)
    formatted_data = pd.concat([data.iloc[1:, 0], data.iloc[1:, 1:].apply(lambda col: col.map(scientific_notation))], axis=1)
    #formatted_data = data.iloc[1:].map(scientific_notation)
    
    # Convert DataFrame to string with right-aligned columns
    formatted_string = formatted_data.to_string(index=False, header=headers, justify='right')
    
    # Save the formatted string to the CSV file
    with open(filepath, 'w') as f:
        f.write(formatted_string)