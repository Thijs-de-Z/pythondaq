from diode_experiment import DiodeExperiment
import matplotlib.pyplot as plt

measurements = DiodeExperiment()

print(measurements.measurements(N = 4, start = 0, stop = 1024))

# plt.errorbar(voltage, current, yerr = c_err, xerr = v_err, markersize = 1, color = 'r', )
# plt.show()