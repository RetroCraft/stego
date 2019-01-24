import filetype
import mmap
from pathlib import Path


def process(f):
    kind = filetype.guess(f)

    with open(f, 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
        # check for data appended to end of file
        if 'png' in kind.mime:
            concat(s, b'IEND\xaeB\x60\x82')
        if 'gif' in kind.mime:
            # gif should end with \x3b. if not, grab concat
            if s[-1] != b';':
                concat(s, b';')
        if 'jpeg' in kind.mime:
            concat(s, b'\xff\xd9')


def concat(s, marker):
    end = s.rfind(marker)
    if end != -1:
        chunk = s[end + len(marker):].decode('utf-8')  # everything after IEND
        data = chunk.strip()
        if data:
            print('[i|concat] found data:')
            print(data)
            print('[i|concat] end found data.')
