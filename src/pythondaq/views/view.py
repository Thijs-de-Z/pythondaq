# primitive view to use for an experiment with an LED and resistor

from pythondaq.models.diode_experiment import DiodeExperiment, init
import matplotlib.pyplot as plt

def i_u_characteristics():

    # requesting of device to use
    print('devices')
    init()
    inpt = input("Please choose the index of the device to use: ")

    N = input("How many measurements do you want to run? ")

    # calling of class
    measurements = DiodeExperiment(inpt)

    # starting of measurements with given values
    measurements.measurements(N = N, start = 0, stop = 1024)

    # getting of values
    current = measurements.get_current()
    voltage = measurements.get_voltage()
    c_err = measurements.get_err_current()
    v_err = measurements.get_err_voltage()

    # plotting of measured data
    plt.errorbar(voltage, current, yerr = c_err, xerr = v_err, markersize = 1, color = 'r', fmt = 'o' )
    plt.show()