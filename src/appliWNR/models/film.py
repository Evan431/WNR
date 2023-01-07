from django.db import models


class Film(models.Model):
    id = models.IntegerField()
    original_title = models.CharField(max_length=100)
    overview = models.CharField(max_length=1000)
    poster_path = models.CharField(max_length=100)
    production_companies = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
