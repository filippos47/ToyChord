import click
import requests
import json

from cli.utils.global_options import global_options

@click.command()
@click.option('--key', '-k', type = str, required = True,
        help = 'The key of the queried key-value pair') 
@global_options
def query(ip_address, port, key):
    url = 'http://' + str(ip_address) + ':' + str(port) + '/query'
    params = { "key": key }
    response = requests.get(url, params = params)
    if key != "*":
        click.echo(response.text)
    else:
        click.echo(json.dumps(response.json(), indent=2))
