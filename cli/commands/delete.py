import click
import requests

from utils.global_options import global_options

@click.command()
@global_options
@click.option('--key', type = str, required = True, help = 'The key of the pair (key, value)') 
def delete(ip_address, port, key):
	url = 'http://' + str(ip_address) + ':' + str(port) + '/delete'
	params = { "key": key }
	response = requests.post(url, params = params)
	return response.text 
