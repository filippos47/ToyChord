import click
import requests
import json

from cli.utils.global_options import global_options

@click.command()
@global_options
def overlay(ip_address, port):
    url = 'http://' + str(ip_address) + ':' + str(port) + '/overlay'
    response = requests.get(url)
    try:
        click.echo(json.dumps(response.json(), indent=2))
    except:
        click.echo(response.text)
