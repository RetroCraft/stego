import ffmpeg
from pathlib import Path
from datetime import timedelta


def spectrogram(f):
    print('[a|spectrogram] generating spectrogram...')
    name = Path(f).stem
    Path('%s' % name).mkdir(exist_ok=True)

    data = ffmpeg.probe(f)
    h, m, s = data['streams'][0]['tags']['DURATION'].split(':')
    length = timedelta(hours=int(h), minutes=int(
        m), seconds=float(s)).total_seconds()
    size = '%sx800' % int(length * 250)

    path = '%s/spectrogram.png' % name
    proc = (
        ffmpeg.input(f)
        .filter('showspectrumpic', s=size, mode='separate')
        .output(path, hide_banner=None, v=0)
        .overwrite_output()
        .run_async()
    )
    return proc
