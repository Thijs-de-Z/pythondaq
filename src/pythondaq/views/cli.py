import click
from pythondaq.models.diode_experiment import DiodeExperiment

@click.group()
def cmd_group():
    pass

@cmd_group.command(
    "list",
)
def listing():
    print('this')
    return


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