from django.db import models

class Programme(models.Model):
	titre = models.CharField(max_length=100)
	titreOriginal = models.CharField(max_length=100)
	affiche = models.CharField(max_length=100)