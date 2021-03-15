import click
import requests

from cli.utils.global_options import global_options

@click.command()
@click.option('--key', '-k', type = str, required = True,
        help = 'The key of the queried key-value pair') 
@global_options
def query(ip_address, port, key):
	url = 'http://' + str(ip_address) + ':' + str(port) + '/query'
	params = { "key": key }
	response = requests.get(url, params = params)
	click.echo(response.text)
