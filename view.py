# primitive view to use for an experiment with an LED and resistor

from diode_experiment import DiodeExperiment
import matplotlib.pyplot as plt
from diode_experiment import init

# requesting of device to use
print('devices')
init()
inpt = input("Please choose the index of the device to use: ")

# calling of class
measurements = DiodeExperiment(inpt)

# starting of measurements with given values
measurements.measurements(N = 10, start = 0, stop = 1024)

# getting of values
current = measurements.get_current()
voltage = measurements.get_voltage()
c_err = measurements.get_err_current()
v_err = measurements.get_err_voltage()

# plotting of measured data
plt.errorbar(voltage, current, yerr = c_err, xerr = v_err, markersize = 1, color = 'r', fmt = 'o' )
plt.show()