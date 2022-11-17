# primitive view to use for an experiment with an LED and resistor
from pythondaq.models.diode_experiment import DiodeExperiment, init
from pythondaq.views.saving import data_to_csv
import matplotlib.pyplot as plt


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
