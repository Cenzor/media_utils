from django.urls import path
from . import views


app_name = 'app_imgtopdf'

urlpatterns = [
    path('', views.upload_file, name='imgtopdf'),
    path('<str:filename>/', views.download_file, name='download_file')
]
