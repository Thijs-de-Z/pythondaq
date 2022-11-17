import click
from pythondaq.models.diode_experiment import DiodeExperiment, init

@click.group()
def cmd_group():
    pass



@cmd_group.command(
    "list",
)
def listing():
    return init()


@cmd_group.command(
    "info",
)
@click.option(
    "-d",
    "--device",
    default = 'none',
    type = str
)
def information(device):
    return init(device)



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
def scanning(begin, end):
    experiment = DiodeExperiment
    results = experiment.scan(begin, end)   # does not work yet
    return print(results)

if __name__ == "__main__":
    cmd_group()