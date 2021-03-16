import click
import requests

from cli.utils.global_options import global_options

@click.command()
@global_options
def join(ip_address, port):
    url = 'http://' + str(ip_address) + ':' + str(port) + '/join'
    response = requests.post(url)
    click.echo(response.text)
