# -*- coding: utf-8 -*-
import asyncio

import click


@click.group()
def commands():
    pass


@click.command()
def init():
    from api_service.config.app import app
    from api_service.config.commands.init import ProjectInitialization

    loop = asyncio.new_event_loop()
    loop.run_until_complete(ProjectInitialization.start(app))


commands.add_command(init)


if __name__ == "__main__":
    commands()
