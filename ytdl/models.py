from django.db import models


class YouTubeDL(models.Model):

    url = models.URLField('URL', default='https://www.youtube.com/watch?v=cwAors_xDA4')
