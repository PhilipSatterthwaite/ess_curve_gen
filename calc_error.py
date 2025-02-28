import pandas as pd
import os
from name_and_save import name_and_save
# create 2d array with species name and maximum error for two sets of data
# input: 2 PDRs outputs for nonpremixed (Y vs Z)
# output: normalized error data

def error_calc(set1, set2, name, directory):
    #set1 is the "more correct" set. i.e. the set that error is normalized by
    set1_subset = set1.iloc[1:, 1:].astype(float)
    set2_subset = set2.iloc[1:, 1:].astype(float)

    norm_factor = set1_subset.max()

    error_subset = set1_subset.apply(lambda x: x.astype(float)) - set2_subset.apply(lambda x: x.astype(float))

    # Concatenate error_subset with the first column from combined DataFrame

    error_normalized = error_subset.div(norm_factor)

    error = pd.concat([set1.iloc[1:, 0], error_normalized], axis=1)
    error_with_titles = pd.concat([set1.iloc[:1, :], error], ignore_index=True)
    name_and_save(error_with_titles, name,directory)
    return error_with_titles

