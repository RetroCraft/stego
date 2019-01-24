import ffmpeg
import asyncio
from pathlib import Path

from stego import audio


def process(f):
    name = Path(f).stem

    # spectro
    spectro = audio.spectrogram(f)

    # split to frames
    Path('%s/frames' % name).mkdir(exist_ok=True)
    print('[v|frames] generating frame-by-frame...')
    frames = (
        ffmpeg.input(f)
        .output('%s/frames/%%04d.png' % name, an=None, hide_banner=None, v=0)
        .overwrite_output()
        .run_async()
    )

    spectro.wait()
    print('[a|spectrogram] done.')
    frames.wait()
    print('[v|frames] done.')
