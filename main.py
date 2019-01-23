#!/usr/bin/env python3
import click
import stego.youtube


@click.group()
def cli():
    pass


@cli.command()
@click.argument('url')
def youtube(url):
    f = stego.youtube.download(url)
    click.echo(f)


@cli.command()
def dropdb():
    click.echo('Dropped the database')


if __name__ == '__main__':
    cli()
