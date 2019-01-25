#!/usr/bin/env python3
import click
import filetype
import re
import requests
from stego import *


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
def f(filename):
    """ process file FILENAME """
    process_file(filename)


@cli.command()
@click.argument('url')
def u(url):
    """ process url URL """
    process_url(url)


def process_file(f):
    kind = filetype.guess(f)
    if kind:
        print('[f] detected filetype %s' % kind.mime)
        if 'video' in kind.mime:
            return video.process(f)
        if 'audio' in kind.mime:
            return audio.process(f)
        if 'image' in kind.mime:
            return image.process(f)
    return print('[f] cannot detect file type.')


def process_url(u):
    # youtube-dl
    try:
        print('[u] attempting youtube-dl...')
        f = youtube.download(url)
        return video.process(f)
    except:
        print('[u] youtube-dl failed.')

    # normal download
    f = ''
    try:
        print('[u] attempting raw download...')
        # determine filename
        r = requests.get(u, allow_redirects=True)
        # find filename
        f = 'download'
        # try url
        if u.find('/'):
            f = u.rsplit('/', 1)[1]
        # try headers
        cd = r.headers.get('content-disposition')
        if cd:
            fname = re.findall('filename=(.+)', cd)
            if len(fname) != 0:
                f = fname[0]
        # save file
        open(f, 'wb').write(r.content)
        print('[u] downloaded to "%s"' % f)
    except:
        print('[u] could not download file.')
    if f:
        return process_file(f)


if __name__ == '__main__':
    cli()
