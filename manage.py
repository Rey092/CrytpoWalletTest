# -*- coding: utf-8 -*-
import asyncio

import click

from config.commands.init import ProjectInitialization
from config.db import SessionLocal


@click.group()
def commands():
    pass


@click.command()
def init():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(ProjectInitialization.start(SessionLocal()))


commands.add_command(init)

if __name__ == "__main__":
    commands()
