import matplotlib.pyplot as plt

def graphing(current, voltage, c_err, v_err):
    """Graphing of given lists of values.

    Args:
        current (list): List with (average) values for current
        voltage (list): List with (average) values for voltage
        c_err (list): Errors on the current
        v_err (list): Errors on the voltage
    """      
    plt.figure()
    plt.title('I,U characteristics of a LED')
    plt.errorbar(voltage, current, yerr = c_err, xerr = v_err, markersize = 1, color = 'r', fmt = 'o' )
    plt.xlim([0, 3.3])
    plt.xlabel('Voltage (U)')
    plt.ylabel('Current (I)')
    plt.show()
