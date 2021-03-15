import click
from functools import wraps

# Nice cheat to set global parameters for every subcommand
# https://github.com/pallets/click/issues/108#issuecomment-194465429
def global_options(f):
    @wraps(f)
    @click.option('--ip_address', '-ip', type=str, required = True,
        help='The IP address of target Chord node')
    @click.option('--port', '-p', type=int, required = True,
        help='The port of target Chord node')
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper
