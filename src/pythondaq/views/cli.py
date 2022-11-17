import click
from pythondaq.models.diode_experiment import DiodeExperiment, init, info, adc_volt

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
def scanning(begin, end, device):


    if device == 'false':
        print('No device has been selected. Please try again')

    elif device not in info():
        print('Device is not available please use >>start_experiment info to see all available devices.')

    else:
        experiment = DiodeExperiment(device)
        begin = adc_volt(begin, 3.3, 2**10)
        end = adc_volt(end, 3.3, 2**10)
        results = experiment.scan(begin, end)
        print(results)


if __name__ == "__main__":
    cmd_group()