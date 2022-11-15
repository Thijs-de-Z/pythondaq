# primitive view to use for an experiment with an LED and resistor

from pythondaq.models.diode_experiment import DiodeExperiment, init
import matplotlib.pyplot as plt
from datetime import date
import os
import pandas as pd

# check if path exists and if writing is allowed
def path_check(path):

    # making new folder for current date if not done already
    if not os.path.exists(path):

        # fixes error if path is non writeable
        try:
            os.makedirs(path)

        except:
            print("Not allowed to write in this path, please change the permissions or run the program through a different path")
            return False
    
    return True


# saving of data in csv file:
def data_to_csv(voltage_w_err, current_w_err):

    # new path with current date
    today = f'{date.today()}'
    path = f'../data/{today}'

    if path_check(path):
        indx = 0

        # new index for new measurement
        for filename in os.listdir(path):
            if filename.endswith(f'measurement_{indx}.csv'):
                indx += 1

        # saving of data
        df = {'voltage': voltage_w_err[0], 'error': voltage_w_err[1], 'current': current_w_err[0], 'error': current_w_err[1]}
        df = pd.DataFrame(df)
        df.to_csv(f'{path}/measurement_{indx}.csv', index = False, sep = ',')


def i_u_characteristic():

    # requesting of device to use
    print('devices')
    init()
    inpt = input("Please choose the index of the device to use: ")

    # requesting amount of measurements
    N = input("How many measurements do you want to take? ")

    # calling of class
    measurements = DiodeExperiment(inpt)

    # starting of measurements with given values
    measurements.measurements(N = int(N), start = 0, stop = 1024)

    # getting of values
    current = measurements.get_current()
    voltage = measurements.get_voltage()
    c_err = measurements.get_err_current()
    v_err = measurements.get_err_voltage()

    # saving of data
    if input("would you like to save the data [Y/N]? ") == 'Y' or 'y':
        data_to_csv([voltage, v_err], [current, c_err])

    # plotting of measured data
    plt.errorbar(voltage, current, yerr = c_err, xerr = v_err, markersize = 1, color = 'r', fmt = 'o' )
    plt.show()
