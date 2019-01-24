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
    frames = (
        ffmpeg.input(f)
        .output('%s/frames/%%04d.png' % name, an=None)
        .overwrite_output()
        .run_async()
    )

    spectro.wait()
    frames.wait()
