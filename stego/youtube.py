import youtube_dl


class YDLLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def download(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mkv',
        'logger': YDLLogger(),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[y|download] beginning download...')
        info_dict = ydl.extract_info(url)
        video_title = info_dict.get('title', None)
        filename = '%s.mkv' % video_title
        print('[y|download] downloaded %s' % filename)
        return filename
