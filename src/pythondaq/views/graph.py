import matplotlib.pyplot as plt

def graph(current, voltage, c_err, v_err):   
    plt.figure()
    plt.title('I,U characteristics of a LED')
    plt.errorbar(voltage, current, yerr = c_err, xerr = v_err, markersize = 1, color = 'r', fmt = 'o' )
    plt.xlim([0, 3.3])
    plt.xlabel('Voltage (U)')
    plt.ylabel('Current (I)')
    plt.show()
