from django.shortcuts import render


def index(request):
    return render(request, 'media_utils/main.html', {'section': ''})
