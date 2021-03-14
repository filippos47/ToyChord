import click

from utils.global_options import global_options
from commands.join import join
from commands.depart import depart
from commands.insert import insert
from commands.delete import delete
from commands.query import query
from commands.overlay import overlay

@click.group(help= "Welcome to the interface of our file sharing application Toychord.Have fun with ToyChord!!")
@global_options
def cli(ip_address, port):
    pass
 
cli.add_command(join)
cli.add_command(depart)
cli.add_command(insert)
cli.add_command(delete)
cli.add_command(query)
cli.add_command(overlay)


if __name__ == '__main__':
  cli()







