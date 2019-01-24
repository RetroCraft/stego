import filetype
import mmap
from pathlib import Path


def process(f):
    kind = filetype.guess(f)

    if 'png' in kind.mime:
        concat(f, b'IEND\xaeB\x60\x82')


def concat(f, marker):
    with open(f, 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
        end = s.find(marker)
        if end != -1:
            chunk = s[end + len(marker):]  # everything after IEND
            print('[i|concat] found data:')
            print(chunk.decode('utf-8'))
            print('[i|concat] end found data.')
