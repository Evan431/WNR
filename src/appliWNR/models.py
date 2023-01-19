from django.db import models
from django.contrib.auth.models import AbstractUser
from WNR.settings import AUTH_USER_MODEL
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class CompagnieProduction(models.Model):
    nom = models.CharField(max_length=100)


class Personne(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    metier = models.CharField(max_length=100)


class Genre(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom}"


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

    def __str__(self):
        return f"{self.titre}"


class Utilisateur(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

    def getListeDejaVue(self):
        if ListeDejaVue.objects.filter(utilisateur=self).exists():
            liste = ListeDejaVue.objects.get(
                utilisateur=self)
        else:
            ListeDejaVue.objects.create(utilisateur=self)
        return liste

    def getMaListe(self):
        if MaListe.objects.filter(utilisateur=self).exists():
            liste = MaListe.objects.get(
                utilisateur=self)
        else:
            liste = []
        return liste

    def noterProgramme(self, programme, note):
        note_obj, _ = Note.objects.get_or_create(
            programme=programme, utilisateur=self)
        if note_obj.note == note:
            note_obj.delete()
        else:
            note_obj.note = note
            note_obj.save()


class Note(models.Model):
    note = models.PositiveIntegerField(null=True)
    utilisateur = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE)
    programme = models.OneToOneField(
        Programme, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('utilisateur', 'programme')

    def __str__(self):
        return f"{self.note} : {self.programme.titre} - {self.utilisateur.username}"


class ListeSuggestion(models.Model):
    utilisateur = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    programmes = models.ManyToManyField(Programme)
    derniereMAJ = models.DateTimeField(auto_now=True)


class ListeDejaVue(models.Model):
    utilisateur = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    programmes = models.ManyToManyField(Programme)

    def __str__(self):
        return f"{self.utilisateur}"


class MaListe(models.Model):
    utilisateur = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    programmes = models.ManyToManyField(Programme)

    def __str__(self):
        return f"{self.utilisateur}"


class Film(Programme):
    duree = models.CharField(max_length=100)

    def __str__(self):
        return f"Film : {self.titre}"


class Serie(Programme):
    nombreSaison = models.IntegerField(default=1)
    nombreEpisodes = models.IntegerField(default=1)
    status = models.CharField(max_length=100)
    dureeMoyEp = models.IntegerField()

    def __str__(self):
        return f"Série : {self.titre}"


class Role(models.Model):
    nom = models.CharField(max_length=100)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    acteur = models.ForeignKey(Personne, on_delete=models.CASCADE)

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def make_hash_value(self, user, timestamp):
        return {
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        }
account_activation_token = AccountActivationTokenGenerator()
