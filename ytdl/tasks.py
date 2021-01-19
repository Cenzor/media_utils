from media_utils.celery import app
import youtube_dl
from django.template import loader
from django.core.mail import send_mail
from media_utils import settings
import os
from datetime import datetime, timedelta


@app.task
def download_video(code, video_url, path, email):
    ydl_opts = {
        'format': code,
        'outtmpl': f'{path}{code}_%(title)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        ydl.download([video_url])
        info_dict = ydl.extract_info(video_url, download=False)
        title = info_dict.get('title')
        ext = ''
        for format_item in info_dict.get('formats'):
            if format_item.get('format_id', 'None') == code:
                ext = format_item.get('ext', 'None')
        filename = code + '_' + title + '.' + ext

        expire_date = datetime.strftime(
            (datetime.now() + timedelta(hours=1)), '%d.%m.%Y %H:%M'
        )
        html_message = loader.render_to_string(
            'ytdl/email.html',
            {
                'filename': filename,
                'expire_date': expire_date
            }
        )
        send_mail(
            'Ссылка для скачаивания',
            'Message',
            'lomakov.k@gmail.com',
            [email],
            fail_silently=False,
            html_message=html_message
        )
        tomorrow = (datetime.utcnow() + timedelta(hours=1))
        remove_expire_file.apply_async((filename,), eta=tomorrow)


@app.task
def remove_expire_file(filename):
    file = settings.MEDIA_ROOT + filename
    try:
        os.remove(file)
    except Exception:
        pass
