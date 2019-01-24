import youtube_dl


def download(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mkv',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url)
        video_title = info_dict.get('title', None)
        return '%s.mkv' % video_title
