from media_utils.celery import app
import youtube_dl


@app.task
def download_video(code, video_url, path):
    ydl_opts = {
        'format': code,
        'outtmpl': f'{path}%(title)s.%(ext)s'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        ydl.download([video_url])
