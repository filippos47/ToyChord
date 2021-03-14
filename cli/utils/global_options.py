import click
from click_params import IP_ADDRESS

_global_options = [
    click.option('--ip_address', '-ip', type=IP_ADDRESS, default="0.0.0.0",
        help='The IP address of target Chord node'),
    click.option('--port', '-p', type=int, default="3333",
        help='The port of target Chord node')
]

# Nice cheat to set global parameters for every subcommand
# https://github.com/pallets/click/issues/108#issuecomment-194465429
def global_options(func):
    for option in reversed(_global_options):
        func = option(func)
    return func
