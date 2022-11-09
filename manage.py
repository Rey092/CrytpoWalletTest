# -*- coding: utf-8 -*-
import asyncio

import click


@click.group()
def commands():
    pass


@click.command()
def init():
    from config.app import app
    from config.commands.init import ProjectInitialization

    loop = asyncio.new_event_loop()
    loop.run_until_complete(ProjectInitialization.start(app))


@click.command()
def ethereum_blocks_parser():
    from apps.network_ethereum.block_parser import get_event

    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_event())


commands.add_command(init)
commands.add_command(ethereum_blocks_parser)


if __name__ == "__main__":
    commands()
