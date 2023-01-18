from django.db import models
from django.contrib.auth.models import AbstractUser
from WNR.settings import AUTH_USER_MODEL


class CompagnieProduction(models.Model):
    nom = models.CharField(max_length=100)


class Personne(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    metier = models.CharField(max_length=100)


class Genre(models.Model):
    nom = models.CharField(max_length=100)


class Programme(models.Model):
    titre = models.CharField(max_length=100)
    titreOriginal = models.CharField(max_length=100)
    bandeAnnonce = models.CharField(max_length=100)
    popularite = models.FloatField()
    affiche = models.CharField(max_length=100)
    listPersonne = models.ManyToManyField(Personne)
    listGenre = models.ManyToManyField(Genre)
    listCompaProd = models.ManyToManyField(CompagnieProduction)
    note_global = models.PositiveIntegerField(null=True)
    description = models.TextField()
    date = models.DateField()


class Utilisateur(AbstractUser):
    pass


class Note(models.Model):
    note = models.PositiveIntegerField(null=True)
    utilisateur = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE)
    programme = models.OneToOneField(
        Programme, on_delete=models.CASCADE)


class ListeSuggestion(models.Model):
    utilisateur = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE)
    programmes = models.ManyToManyField(Programme)
    derniereMAJ = models.DateTimeField(auto_now=True)


class ListeDejaVue(models.Model):
    utilisateur = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE)
    programmes = models.ManyToManyField(Programme)


class MaListe(models.Model):
    utilisateur = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE)
    programme = models.ManyToManyField(Programme)


class Film(Programme):
    duree = models.CharField(max_length=100)


class Serie(Programme):
    nombreSaison = models.IntegerField(default=1)
    nombreEpisodes = models.IntegerField(default=1)
    status = models.CharField(max_length=100)
    dureeMoyEp = models.IntegerField()


class Role(models.Model):
    nom = models.CharField(max_length=100)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    acteur = models.ForeignKey(Personne, on_delete=models.CASCADE)
