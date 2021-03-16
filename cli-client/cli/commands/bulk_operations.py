import click
import requests

from cli.utils.global_options import global_options
from .join import join
from .depart import depart
from .overlay import overlay
from .insert import insert
from .delete import delete
from .query import query
from random import randrange

@click.command()
@click.option('--source_file', '-f', type = str, required = True,
        help = 'File which contains desired operations, one per line. Format' \
               ' should be `<OPERATION>, [<KEY>], [<VALUE>]`')
@global_options
@click.pass_context
def bulk_operations(ctx, ip_port_list, source_file): #[(ip1,port1),(ip2,port2) ] 
    with open(source_file, "r") as fp:
        for line in fp.readlines():
            arguments = [ x.strip() for x in line.split(',') ]
            command = arguments[0]
            random_node=randrange(len(ip_port_list))
            random_ip=random_node[0]
            random_port=random_node[1]
            if command == "join":
                ctx.invoke(join, ip_address = random_ip,port=random_port)
            elif command == "depart":
                ctx.invoke(depart, ip_address = random_ip,port=random_port)
            elif command == "overlay":
                ctx.invoke(overlay, ip_address = random_ip,port=random_port)
            elif command == "insert":
                ctx.invoke(insert, ip_address = random_ip,port=random_port,
                        key = arguments[1], value = arguments[2])
            elif command == "delete":
                ctx.invoke(delete, ip_address = random_ip,port=random_port,
                        key = arguments[1])
            elif command == "query":
                ctx.invoke(query, ip_address = random_ip,port=random_port,
                        key = arguments[1])
