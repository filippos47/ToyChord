import click
import requests

from cli.utils.global_options import global_options

@click.command()
@click.option('--key', '-k', type = str, required = True,
        help = 'The key of the to-be-inserted key-value pair') 
@click.option('--value', '-v', type = str, required = True,
        help = 'The value of the to-be-inserted key-value pair') 
@global_options
def insert(ip_address, port, key, value):
	url = 'http://' + str(ip_address) + ':' + str(port) + '/insert'
	params = { "key": key, "value": value }
	response = requests.post(url, params = params)
	click.echo(response.text)
