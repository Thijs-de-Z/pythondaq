import click
from pythondaq.models.diode_experiment import DiodeExperiment, init, info
from pythondaq.views.saving import data_to_csv
from pythondaq.views.graph import graphing
import math
import numpy as np
#TODO
# Work out the fitting of the Shockley model

def experiment_start(begin, end, device, repeats, save, graph, printing):
    """Runs the experiment(s) for the diode with the given arguments.

    Args:
        begin (float): Start voltage
        end (float): End voltage 
        device (str): Identification string of the device to use
        repeats (int): Amount of times to run the experiment. If =1 no errors are calculated
        save (str): Filename to save the data to. Defaults to "none" saving no data
        graph (bool): Argument to show the graph of the experiment(s)
        fit (bool): Argument to fit the result to the Shockley model.
        printing (bool): Argument to print the results in the terminal.
    """    
    experiment = DiodeExperiment(device)
    experiment.measurements(N=repeats, start=begin, stop=end)

    current = experiment.get_current()
    voltage = experiment.get_voltage()
    c_err = experiment.get_err_current()
    v_err = experiment.get_err_voltage()

    if save != "none":
        data_to_csv(voltage_w_err=[voltage, v_err], current_w_err=[current, c_err], filename=save)
    
    if graph:
        graphing(current=current, voltage=voltage, c_err=c_err, v_err=v_err)

    if printing:
        print(f"The measured voltage is: {current}")
        print(f"With its error: {np.array(c_err)}")
        print(f"The calculated current is: {current}")
        print(f"With its error: {np.array(c_err)}")


def device_id_string(string):
    """Searches in visible devices if they contain a search string.

    Args:
        string (str): Search string to search for in visible devices

    Returns:
        list: Devices containing the requested search string
    """    
    devices = []
    for i in info():
        if i.__contains__(string):
            devices.append(i)

    return devices

def model(x, a, b):
    return a * (math.e ** (x / b) - 1)



@click.group()
def cmd_group():
    """Making of terminal command group
    """    
    pass


@cmd_group.command(
    "list",
)
@click.option(
    "-s",
    "--search",
    default = "",
    type = str,
    help = "Search for devices with the given search string",
    show_default = True,
)
def listing(search):
    """Requests a list of all visible devices and their identification\f
    Args:
        search (str): search string to identify devices containg this string.
    """
    devices = device_id_string(search)

    if search == "":
        print("No search string given shwoing all devices.")
        print(info())

    elif len(devices) == 0:
        print("No devices contains that search string!")

    else:
        print("These devices matched your search term:")
        for j in devices:
            print(j)


@cmd_group.command(
    "info"
)
@click.option(
    "-d",
    "--device",
    default = "true",
    type = str,
    help = "Device or search string to request information from.",
    show_default = True,
)
def information(device):
    """Returns the information of the device. If no argument is given it returns information of all devices.\f
    Args:
        device (str): Device/search string of which information is requested.
    """
    devices = device_id_string(device)

    if device == "true":
        print("No search string given. Showing all devices")
        init(device)

    elif len(devices) == 0:
        print("No devices contains that search string!")
    
    else:
        print("Information of devices which contain the search string:")
        for i in devices:
            init(i)


@cmd_group.command(
    "scan",
)
@click.option(
    "-b",
    "--begin",
    default = 0,
    type = click.FloatRange(0, 3.3),
    help = "Starting value of measurements in volts.",
    show_default = True,
)
@click.option(
    "-e",
    "--end",
    default = 3.3,
    type = click.FloatRange(0, 3.3),
    help = "Ending value of measurements in volts.",
    show_default = True,
)
@click.option(
    "-d",
    "--device",
    default = 'false',
    type = str,
    help = "Device to use, input can be its identification string, index or search string.",
    show_default = True
)
@click.option(
    "-r",
    "--repeats",
    default = 1,
    type = int,
    help = "Amount of experiments to run.",
    show_default = True,
)
@click.option(
    "-s",
    "--save",
    default = "none",
    type = str,
    help = "Filename to save the data to. If none is given do not save",
    show_default = True,
)
@click.option(
    "--graph/--no-graph",
    default = False,
    type = bool,
    help = "Option to show a graph visualising the data",
    show_default = True,
)
@click.option(
    '--index/--no-index',
    default = False,
    type = bool,
    help = "Option to choose the index of the device to use instead of its identification string",
    show_default = True,
)
@click.option(
    '--printing/--no-printing',
    default = False,
    type = bool,
    help = "Optrion to print the results",
    show_default = True,
)
def scanning(begin, end, device, repeats, save, graph, index, printing):
    """Measures the i,u characteristics of a diode.\f

    Args:
        begin (float): Starting value of measurements in volts. Default is 0
        end (float): Ending value of measurements in volts. Default is 3.3
        device (str): Device to use, input can be its identification string, index or search string.
        repeats (int): Amount of experiments to run. Default is 1
        save (str): Filename to save the data to. If none is given do not save.
        graph (bool): Option to show a graph visualising the data. Default is False
        index (bool): Option to use index of device instead of its identification string. Default is False
        fit (bool): Option to fit the result to the Shockley model.
        print (bool): Option to print the results in the terminal.
    """

    devices = device_id_string(device)   
    if device == 'false':                               # if no device is given
        print('No device has been selected. Please try again')

    elif device.isdigit() and index:                    # if device index is used instead of its identification/search string
        try:
            experiment_start(begin=begin, end=end, device=info()[int(device)], repeats=repeats, save=save
                                , graph=graph, printing=printing)

        except:
            print("Unexpected error occured, please check if the right device is chosen or try using less options. (fit option not functionable yet)")

    elif len(devices) == 0:                             # if no devices contain the search string
        print('No Device contains that search string!')

    elif len(devices) > 1:                              # if multiple devices contain the search string
        print('Multiple devices contain that search string. Please be more specific')
        print('Devices containing that search string:')
        for i in devices:
            init(i)

    else:                                               
        device = devices[0]
        try:
            experiment_start(begin=begin, end=end, device=device, repeats=repeats, save=save
                            , graph=graph, printing=printing)
        except:
            print("Unexpected error occured, please check if the right device is chosen.")


if __name__ == "__main__":
    cmd_group()