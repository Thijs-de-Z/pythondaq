import click
from pythondaq.models.diode_experiment import DiodeExperiment, init, info


def experiment_start(begin, end, device, repeats, output, graph):
    if device.isdigit():
        experiment = DiodeExperiment(info()[int(device)])
    else:
        experiment = DiodeExperiment(device)
      
    results = experiment.scan(begin, end)


    experiment.device.close_device()
    pass

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
    "-repeats",
    "--repeats",
    default = 1,
    type = int,
    show_default = True,
)
@click.option(
    "-o",
    "--output",
    default = "/today",
    type = str,
    show_default = True,
)
@click.option(
    "--graph/--no-graph",
    default = False,
    type = bool,
    show_default = True,
)
def scanning(begin, end, device, repeats, output, graph):
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
            experiment_start(begin=begin, end=end, device=device, repeats=repeats, output=output
                            , graph=graph)

        except:
            print('Device is not available please use ">>start_experiment info" to see all available devices.')

    elif device not in info():
        print('Device is not available please use ">>start_experiment info" to see all available devices.')

    else:
        experiment_start(begin=begin, end=end, device=device, repeats=repeats, output=output
                        , graph=graph)


if __name__ == "__main__":
    cmd_group()