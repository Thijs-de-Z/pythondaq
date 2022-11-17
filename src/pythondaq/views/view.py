# primitive view to use for an experiment with an LED and resistor
from pythondaq.models.diode_experiment import DiodeExperiment, init
import matplotlib.pyplot as plt
from datetime import date
import os
import pandas as pd


def path_check(path):
    """Checks if the path exists and is writable

    Args:
        path (string): Path to check the existanse and writablity of the path

    Returns:
        boolean: True/False dependent if the path is writable
    """    

    if not os.path.exists(path):

        try:
            os.makedirs(path)

        except:
            print("Not allowed to write in this path, please change the permissions or run the program through a different path")
            return False
    
    return True


def data_to_csv(voltage_w_err, current_w_err):
    """Saves the data into a csv file. This csv file will automaticly create a folder, data, in the parent file if this does not exist already.
    The data is saved within seperate folders with the date when the experiment was conducted and it will also prevent overwriting previous saved data.

    Args:
        voltage_w_err (list): 2 lists with the voltage of the experiment and it's error
        current_w_err (list): 2 lists with the current of the experiment and it's error
    """    

    today = f'{date.today()}'
    path = f'../data/{today}'

    if path_check(path):
        indx = 0

        for filename in os.listdir(path):
            if filename.endswith(f'measurement_{indx}.csv'):
                indx += 1

        df = {'voltage': voltage_w_err[0], 'error': voltage_w_err[1], 'current': current_w_err[0], 'error': current_w_err[1]}
        df = pd.DataFrame(df)
        df.to_csv(f'{path}/measurement_{indx}.csv', index = False, sep = ',')


def i_u_characteristic():
    """Calculates the I,U characteristics of a diode by running and experiment N times.
    It will automatically show a visual presentation of the I,U characteristics with errors(if N>1).
    Has the option to save the data to a csv file.
    Setting of device and number of experiments is done through a text interface.
    """    

    print('devices')
    init()
    inpt = input("Please choose the index of the device to use: ")

    N = input("How many measurements do you want to take? ")

    measurements = DiodeExperiment(inpt)

    measurements.measurements(N = int(N), start = 0, stop = 1024)

    current = measurements.get_current()
    voltage = measurements.get_voltage()
    c_err = measurements.get_err_current()
    v_err = measurements.get_err_voltage()

    if input("would you like to save the data [Y/N]? ") == 'Y' or 'y' or 'yes':
        data_to_csv([voltage, v_err], [current, c_err])

    plt.errorbar(voltage, current, yerr = c_err, xerr = v_err, markersize = 1, color = 'r', fmt = 'o' )
    plt.show()          # still have to make the graph visuals better
