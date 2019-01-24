#!/usr/bin/env python3
import click
import stego.video
import stego.youtube


@click.group()
def cli():
    pass


@cli.command()
@click.argument('url')
def youtube(url):
    f = stego.youtube.download(url)
    # pass off to video handler function
    video(f)


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
def video(filename):
    stego.video.process(filename)


if __name__ == '__main__':
    cli()
