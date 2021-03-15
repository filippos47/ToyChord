import click
import requests

from cli.utils.global_options import global_options

@click.command()
@global_options
def overlay(ip_address, port):
	url = 'http://' + str(ip_address) + ':' + str(port) + '/overlay'
	response = requests.get(url)
	click.echo(response.text)
