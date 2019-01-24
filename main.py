#!/usr/bin/env python3
import click
import filetype
import re
import requests
import stego.audio
import stego.image
import stego.video
import stego.youtube


@click.command()
@click.option('-f', '--file', 'filename', type=click.Path(exists=True))
@click.option('-u', '--url')
def cli(filename, url):
    if filename:
        return process_file(filename)
    elif url:
        # youtube-dl
        try:
            print('[u] attempting youtube-dl...')
            f = stego.youtube.download(url)
            return stego.video.process(f)
        except:
            print('[u] youtube-dl failed.')

        # normal download
        f = ''
        try:
            print('[u] attempting raw download...')
            # determine filename
            f = process_url(url)
        except:
            print('[u] could not download file.')
        if f:
            return process_file(f)

    print('[ ] nothing to do. specify -f filename or -u URL')


def process_file(f):
    kind = filetype.guess(f)
    if kind:
        print('[f] detected filetype %s' % kind.mime)
        if 'video' in kind.mime:
            return stego.video.process(f)
        if 'audio' in kind.mime:
            return stego.audio.process(f)
        if 'image' in kind.mime:
            return stego.image.process(f)
    return print('[f] cannot detect file type.')


def process_url(u):
    r = requests.get(u, allow_redirects=True)
    # find filename
    filename = 'download'
    # try url
    if u.find('/'):
        filename = u.rsplit('/', 1)[1]
    # try headers
    cd = r.headers.get('content-disposition')
    if cd:
        fname = re.findall('filename=(.+)', cd)
        if len(fname) != 0:
            filename = fname[0]
    # save file
    open(filename, 'wb').write(r.content)
    return filename


if __name__ == '__main__':
    cli()
