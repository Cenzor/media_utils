from django.shortcuts import render


def index(request):
    return render(request, 'ytdl/main.html', {'section': 'ytdl'})
