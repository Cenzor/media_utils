from django.urls import path, re_path
from . import views
from .views import YouTubeDLView


app_name = 'app_ytdl'

urlpatterns = [
    path('', YouTubeDLView.as_view(), name='ytdl'),
    re_path(r'download-order/(?P<video_url>.+)/$',
            views.download_order, name='download_order'),
]
