import click
from pythondaq.models.diode_experiment import DiodeExperiment, init, info
from pythondaq.views.saving import data_to_csv
from pythondaq.views.graph import graphing


def experiment_start(begin, end, device, repeats, save, graph):
    """Runs the experiment(s) for the diode with the given arguments.

    Args:
        begin (float): Start voltage
        end (float): End voltage 
        device (str): Identification string of the device to use
        repeats (int): Amount of times to run the experiment. If =1 no errors are calculated
        save (str): Filename to save the data to. Defaults to "none" saving no data
        graph (bool): Argument to show the graph of the experiment(s)
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
    default = f"{info()}",
    type = str,
    help = "Search for devices with the given search string",
    show_default = True,
)
def listing(search):
    """Requests a list of all visible devices and their identification\f
    Args:
        search (str): search string to identify devices containg this string.

    Returns:
        list: Returns a list of the requested devices
    """    
    devices = []
    for i in info():
        if i.__contains__(search):
            devices.append(i)

    if len(devices) == 0:
        print("No devices matched with that search term!")

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
    help = "Device to request information from.",
    show_default = True,
)
def information(device):
    """Returns the information of the device. If no argument is given it returns information of all devices.\f
    Args:
        device (str): Device of which information is requested.
    """
    init(device)


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
    help = "Device to use, input can be its identification string or index in the list of devices.",
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
def scanning(begin, end, device, repeats, save, graph):
    """Measures the i,u characteristics of a diode.\f

    Args:
        begin (float): Begin voltage in volts
        end (float): End voltage in volts
        device (int, str): Identification of the device. Can be the identification string or its index in the list of devices.
    """    

    if device == 'false':
        print('No device has been selected. Please try again')

    elif device.isdigit():
        try:
            experiment_start(begin=begin, end=end, device=info()[int(device)], repeats=repeats, save=save
                                , graph=graph)

        except:
            print('Device is not available please use ">>cli info" to see all available devices.')

    elif device not in info():
        print('Device is not available please use ">>cli info" to see all available devices.')

    else:
        experiment_start(begin=begin, end=end, device=device, repeats=repeats, save=save
                        , graph=graph)


if __name__ == "__main__":
    cmd_group()