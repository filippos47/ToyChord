import click
import requests
from random import randrange

from .insert import insert
from .delete import delete
from .query import query

@click.command()
@click.option('--source_file', '-f', type = str, required = True,
        help = 'File which contains desired operations, one per line. Format' \
               ' should be `<OPERATION>, [<KEY>], [<VALUE>]`')
# ip1:port1,ip2:port2...(string)
@click.option('--addr_string', '-addr_s', type = str, required = True)
@click.pass_context
def bulk_operations(ctx, source_file, addr_string):
    with open(source_file, "r") as fp:
        for line in fp.readlines():
            arguments = [ x.strip() for x in line.split(',') ]
            command = arguments[0]

            addr_list=addr_string.split(",") 
            for i in range(len(addr_list)):
                  addr_list[i]=addr_list[i].split(":")
            random_node=addr_list[randrange(len(addr_list))]
            random_ip=random_node[0]
            random_port=random_node[1]

            if command == "insert":
                ctx.invoke(insert, ip_address = random_ip, port = random_port,
                        key = arguments[1], value = arguments[2])
            elif command == "delete":
                ctx.invoke(delete, ip_address = random_ip, port = random_port,
                        key = arguments[1])
            elif command == "query":
                ctx.invoke(query, ip_address = random_ip, port = random_port,
                        key = arguments[1])
