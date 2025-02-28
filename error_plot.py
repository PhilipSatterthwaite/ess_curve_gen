
import pandas as pd
import matplotlib.pyplot as plt

def error_plot(error_df, col, xlabel: str=None, ylabel: str=None, title: str=None, legend: bool=False, xlog: bool = False, ylog: bool = False):
    error_vals = error_df.iloc[1:, :]
    
    # Plot the selected columns against column 1
    
    for i in range(len(col)):
        plt.plot(error_vals.iloc[:,0].astype(float), error_vals.iloc[:,col[i]].astype(float), label=error_df.iloc[0, col[i]])

    # Add labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if legend == True:
        plt.legend()
    if xlog == True:
        plt.xscale('log')
    if ylog == True:
        plt.yscale('log')

    # Show plot
    plt.show()