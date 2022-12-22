from django.db import models

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
    note : models.PositiveIntegerField(max_length=10)

class Role(models.Model) : 
    nom = models.CharField(max_length=100)

class Programme(models.Model):
    titre = models.CharField(max_length=100)
    titreOriginal = models.CharField(max_length=100)
    bandeAnnonce = models.CharField(max_length=100)
    popularite = models.FloatField()
    affiche = models.CharField(max_length=100)
    video = models.CharField(max_length=100)
    id = models.IntegerField(max_length=100)
    listRealisateur = models.ManyToManyField(Realisateur)
    listGenre = models.ManyToManyField(Genre)
    listCompaProd = models.ManyToManyField(CompagnieProduction)
    listActeur = models.ManyToManyField(Acteur, through='Role')
    
    class Meta:
        abstract = True

class Utilisateur(models.Model):
    pseudo = models.CharField(max_length=20)
    adresseMail = models.EmailField(max_length=40)
    motDePase = models.CharField(max_length=60) 
    recevoirMail = models.BooleanField()
    cgu = models.BooleanField()

class Film(Programme):
    duree = models.CharField(max_length = 100)

class Serie(Programme):
    nombreSaison = models.IntegerField(max_length = 10)
    nombreEpisodes = models.IntegerField(max_length = 10)
    status = models.CharField(max_length = 100)
    dureeMoyEp = models.IntegerField(max_length = 10)



