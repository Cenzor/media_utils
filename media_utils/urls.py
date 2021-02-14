from django.contrib import admin
from django.urls import path, include
from . import global_view
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from django.views.generic.base import TemplateView


sitemaps = {'static': StaticViewSitemap}

urlpatterns = [
    path('', global_view.index, name='main_index'),
    path('admin/', admin.site.urls),
    path('imgtopdf/', include('imgtopdf.urls'), name='imgtopdf'),
    path('ytdl/', include('ytdl.urls'), name='ytdl'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt',
         TemplateView.as_view(template_name="robots.txt",
                              content_type="text/plain")),
]
