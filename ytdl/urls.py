from django.urls import path
from . import views


app_name = 'app_ytdl'

urlpatterns = [
    path('', views.index, name='ytdl'),
]
