from django.conf import settings
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadImageForm
import os
import mimetypes
from PIL import Image


def upload_file(request):
    sent = False
    file_name_pdf = ''
    if request.method == 'POST':
        upload_form = UploadImageForm(request.POST, request.FILES)
        if upload_form.is_valid():
            file_name = request.FILES['file'].name
            handle_uploaded_file(request.FILES['file'], file_name)
            _, extension = os.path.splitext(file_name)
            file_name_pdf = file_name.replace(extension, '.pdf')
            sent = True
    else:
        upload_form = UploadImageForm()
    return render(request, 'imgtopdf/main.html',
                  {'upload_form': upload_form, 'sent': sent,
                   'section': 'imgtopdf', 'file_name_pdf': file_name_pdf})


def handle_uploaded_file(f, fn):
    with open(settings.MEDIA_ROOT+fn, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    image = Image.open(settings.MEDIA_ROOT+fn)
    image_conv = image.convert('RGB')
    _, extension = os.path.splitext(fn)
    fn_pdf = fn.replace(extension, '.pdf')
    image_conv.save(settings.MEDIA_ROOT+fn_pdf)
    os.remove(settings.MEDIA_ROOT+fn)


def download_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            mime_type, _ = mimetypes.guess_type(file_path)
            response = HttpResponse(fh.read(), content_type=mime_type)
            response['Content-Disposition'] = 'filename=' + \
                os.path.basename(file_path)
            os.remove(file_path)
            return response
    else:
        return HttpResponseRedirect('/imgtopdf/')
