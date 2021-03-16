import click
import requests

from cli.utils.global_options import global_options

@click.command()
@click.option('--key', '-k', type = str, required = True,
        help = 'The key of the to-be-deleted key-value pair')
@global_options
def delete(ip_address, port, key):
    url = 'http://' + str(ip_address) + ':' + str(port) + '/delete'
    params = { "key": key }
    response = requests.post(url, params = params)
    click.echo(response.text)
