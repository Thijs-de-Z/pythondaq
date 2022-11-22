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
def listing():
    """Requests a list of all visible devices and their identification

    Returns:
        list: Returns a list of visible devices
    """    
    return print(info())


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
        device (str): Device of which information is requested
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
    show_default = True,
)
@click.option(
    "-e",
    "--end",
    default = 3.3,
    type = click.FloatRange(0, 3.3),
    show_default = True,
)
@click.option(
    "-d",
    "--device",
    default = 'false',
    type = str,
    show_default = True
)
@click.option(
    "-r",
    "--repeats",
    default = 1,
    type = int,
    show_default = True,
)
@click.option(
    "-s",
    "--save",
    default = "none",
    type = str,
    show_default = True,
)
@click.option(
    "--graph/--no-graph",
    default = False,
    type = bool,
    show_default = True,
)
def scanning(begin, end, device, repeats, save, graph):
    """Performs a single scan. The begin and end voltage can be given and the device can be given (index and string identification works)\f

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