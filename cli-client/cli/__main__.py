import click

from cli.utils.global_options import global_options
from cli.commands.join import join
from cli.commands.depart import depart
from cli.commands.insert import insert
from cli.commands.delete import delete
from cli.commands.query import query
from cli.commands.overlay import overlay
from cli.commands.bulk_operations import bulk_operations

@click.group(help= 'Welcome to the interface of our file sharing application ' \
                   'Toychord. Have fun with ToyChord!!')
def cli():
    pass
 
cli.add_command(join)
cli.add_command(depart)
cli.add_command(insert)
cli.add_command(delete)
cli.add_command(query)
cli.add_command(overlay)
cli.add_command(bulk_operations)

if __name__ == '__main__':
    cli()
