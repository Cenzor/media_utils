from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponse, HttpResponseNotFound
import mimetypes
import os
from urllib.parse import quote, unquote
from .forms import YouTubeDLForm, FormatVideoForm
from .tasks import download_video
import youtube_dl


def get_url_info(url):
    """
    Запрашивает информацию о видео.
    Возвращает сформированный список с форматами видео
    """
    ydl_opts = {
    }
    video_format_choices = []
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        info_dict = ydl.extract_info(url, download=False)
        for n, format_item in enumerate(info_dict.get('formats')):
            extension = format_item.get('ext', 'None')
            file_size = format_item.get('filesize')
            if file_size:
                file_size = str(round(file_size/1024/1024, 2))+'Mb'
            else:
                file_size = 'None'
            format_code = format_item.get('format', '')
            acodec = format_item.get('acodec')
            if acodec == 'none':
                acodec = 'Без звука'
            format_id = format_item.get('format_id')
            format_select = format_code + ', ' + extension + ', ' \
                + file_size + ', ' + acodec
            video_format_choices.append((format_id, format_select))
    return video_format_choices


def get_title_and_thumbnail_url(url):
    """
    Запрашивает информацию о видео.
    Возвращает название видео и ссылку на миниатюру видеофайла
    """
    ydl_opts = {

    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        info_dict = ydl.extract_info(url, download=False)
        return (info_dict.get('title'),
                info_dict.get('thumbnails')[0].get('url'))


def download_order(request, video_url):
    """
    Скачивает видео
    """
    video_url = unquote(video_url)
    code = request.POST.get('format_video')
    email = request.POST.get('email')
    download_video.delay(code, video_url, email)
    return render(request, 'ytdl/download_order.html',
                  context={
                      'email': email, 'section': 'ytdl'
                  })


def download_file(request, filename):
    """
    Скачивает ранее загруженный файл
    Если срок ожидания истёк, то возвращает 404
    """
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            mime_type, _ = mimetypes.guess_type(file_path)
            response = HttpResponse(fh.read(), content_type=mime_type)
            response['Content-Disposition'] = 'filename=' + \
                os.path.basename(file_path)
            return response
    else:
        return HttpResponseNotFound('<h1>Время хранения файла истекло</h1>')


class YouTubeDLView(View):
    def get(self, request):
        youtube_form = YouTubeDLForm()
        return render(request, 'ytdl/main.html',
                      {
                          'youtube_form': youtube_form, 'sent': False,
                          'section': 'ytdl'
                      })

    def post(self, request):
        youtube_form = YouTubeDLForm(request.POST)
        if youtube_form.is_valid():
            url = youtube_form.cleaned_data['url']
            title_video, thumbnail_url = get_title_and_thumbnail_url(url)
            choices = get_url_info(url)
            format_form = FormatVideoForm(choices)
            return render(request, 'ytdl/submit.html',
                          {
                              'format_form': format_form, 'section': 'ytdl',
                              'title_video': title_video,
                              'thumbnail_url': thumbnail_url,
                              'video_url': quote(url)
                          })
