from django.db import models


class YouTubeDL(models.Model):

    url = models.URLField('URL')
