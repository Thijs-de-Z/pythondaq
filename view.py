from diode_experiment import DiodeExperiment
import matplotlib.pyplot as plt
from diode_experiment import init

print('devices')
init()
inpt = input("Please choose the index of the device to use: ")

measurements = DiodeExperiment(inpt)

voltage, c_err, current, v_err = measurements.measurements(N = 1, start = 0, stop = 1024)

plt.errorbar(current, voltage, yerr = c_err, xerr = v_err, markersize = 1, color = 'r', fmt = 'o' )
plt.show()