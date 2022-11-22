import os
from datetime import date
import os
import pandas as pd

def path_check(path):
    """Checks if the path exists and is writable

    Args:
        path (string): Path to check the existanse and writablity of the path

    Returns:
        bool: True/False dependent if the path is writable
    """    
    if not os.path.exists(path):

        try:
            os.makedirs(path)

        except:
            print("Not allowed to write in this path, please change the permissions or run the program through a different path")
            return False
    
    return True


def data_to_csv(voltage_w_err, current_w_err, filename = None):
    """Saves the data into a csv file. This csv file will automaticly create a folder, data, in the parent file if this does not exist already.
    The data is saved within seperate folders with the date when the experiment was conducted and it will also prevent overwriting previous saved data.

    Args:
        voltage_w_err (list): 2 lists with the voltage of the experiment and it's error
        current_w_err (list): 2 lists with the current of the experiment and it's error
        filename (bool, str): Name of the file to save data to. If none is given save it to a file with todays date. Defaults to None
    """    
    today = f'{date.today()}'
    path = f'../data/{today}'

    if path_check(path):
        indx = 0
        df = {'voltage': voltage_w_err[0], 'error': voltage_w_err[1], 'current': current_w_err[0], 'error': current_w_err[1]}
        df = pd.DataFrame(df)
        
        # automatic saving if function is called without filename
        if filename == None:
            print("No filename given, saving to standard file.")
            for filename in os.listdir(path):
                if filename.endswith(f'measurement_{indx}'):
                    indx += 1

            df.to_csv(f'{path}/{name}.csv', index = False, sep = ',')
            
        else:
            name = filename
            if f'{name}.csv' in os.listdir(path):
                if input("File already exists. Would you like to overwrite it [Y/N]?") == 'y' or 'Y' or 'yes':
                    df.to_csv(f'{path}/{name}.csv', index = False, sep = ',')

            else:
                df.to_csv(f'{path}/{name}.csv', index = False, sep = ',')
            