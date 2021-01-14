from django.db import models


url = 'https://www.youtube.com/watch?v=_bTf3WJo-2Q'


class YouTubeDL(models.Model):

    url = models.URLField('URL', default=url)
