from django.db import models
from django.contrib.auth.models import AbstractUser
from WNR.settings import AUTH_USER_MODEL

class CompagnieProduction(models.Model) :
    nom = models.CharField(max_length = 100)

class Realisateur(models.Model) :
     nom = models.CharField(max_length=100)
     prenom = models.CharField(max_length=100)
    
class Acteur(models.Model) :
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

class Genre(models.Model) :
    nom = models.CharField(max_length=100)

class Note(models.Model) : 
    note : models.PositiveIntegerField()

class Programme(models.Model):
    titre = models.CharField(max_length=100)
    titreOriginal = models.CharField(max_length=100)
    bandeAnnonce = models.CharField(max_length=100)
    popularite = models.FloatField()
    affiche = models.CharField(max_length=100)
    video = models.CharField(max_length=100)
    listRealisateur = models.ManyToManyField(Realisateur)
    listGenre = models.ManyToManyField(Genre)
    listCompaProd = models.ManyToManyField(CompagnieProduction)
    listActeur = models.ManyToManyField(Acteur, through='Role')

class Utilisateur(AbstractUser):
    pass

class Liste(models.Model):
    utilisateur = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    programme = models.ManyToManyField(Programme)

class ListeDejaVue(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    programme = models.ManyToManyField(Programme)

class MaListe(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    programme = models.ManyToManyField(Programme)

class Film(Programme):
    duree = models.CharField(max_length = 100)

class Serie(Programme):
    nombreSaison = models.IntegerField(default=1)
    nombreEpisodes = models.IntegerField(default=1)
    status = models.CharField(max_length = 100)
    dureeMoyEp = models.IntegerField()

class Role(models.Model) : 
    nom = models.CharField(max_length=100)
    # serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    # film = models.ForeignKey(Film, on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    acteur = models.ForeignKey(Acteur, on_delete=models.CASCADE)



