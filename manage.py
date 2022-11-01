# -*- coding: utf-8 -*-
import asyncio

import click

from config.app import app
from config.commands.init import ProjectInitialization


@click.group()
def commands():
    pass


@click.command()
def init():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(ProjectInitialization.start(app))


commands.add_command(init)

if __name__ == "__main__":
    commands()
