import click
import requests

from utils.global_options import global_options

@click.command()
@global_options
@click.option('--key', type = str, required = True, help = 'The key of the pair (key, value)') 
@click.option('--value', type = str, required = True, help = 'The value of the pair (key, value)') 
def insert(ip_address, port, key, value):
	url = 'http://' + str(ip_address) + ':' + str(port) + '/insert'
	params = { "key": key, "value": value }
	response = requests.post(url, params = params)
	return response.text

