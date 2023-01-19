from django.db import models
from django.contrib.auth.models import AbstractUser
from WNR.settings import AUTH_USER_MODEL


class CompagnieProduction(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom}"


class Personne(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    metier = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} {self.prenom} : {self.metier}"


class Genre(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom}"


class Plateforme(models.Model):
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
    listPlateforme = models.ManyToManyField(Plateforme)
    note_global = models.PositiveIntegerField(null=True)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.titre}"

    def majNote(self):
        print(self)
        notes = [n.note for n in Note.objects.filter(programme=self).all()]
        nbNote = len(notes)
        print(notes)
        print(nbNote)
        if nbNote > 0:
            self.note_global = sum(notes)/nbNote
            self.save()


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
            MaListe.objects.create(utilisateur=self)
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
    utilisateur = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, unique=False)
    programme = models.ForeignKey(
        Programme, on_delete=models.CASCADE, unique=False)

    class Meta:
        unique_together = ('utilisateur', 'programme')

    def __str__(self):
        return f"{self.note} : {self.programme.titre} - {self.utilisateur.username}"


class ListeSuggestion(models.Model):
    utilisateur = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    programmes = models.ManyToManyField(Programme)
    derniereMAJ = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.utilisateur}"


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
    duree = models.IntegerField()

    def __str__(self):
        return f"Film : {self.titre}"

    def getListeFiltre():
        annees = sorted(list(set([annee.year for annee in Film.objects.all(
        ).values_list('date', flat=True).distinct()])), reverse=True)
        durees = {'< 30 min': (0, 30), '30min - 1h': (30, 60), '1h - 1h30': (60, 90), '1h30 - 2h': (
            90, 120), '2h - 2h30': (120, 150), '2h30 - 3h': (150, 180), '> 3h': (180, 99999999)}
        genres = Film.objects.values_list(
            'listGenre__nom', flat=True).distinct()
        return annees, durees, genres


class Serie(Programme):
    nombreSaison = models.IntegerField(default=1)
    nombreEpisodes = models.IntegerField(default=1)
    status = models.CharField(max_length=100)
    dureeMoyEp = models.IntegerField()

    def __str__(self):
        return f"Série : {self.titre}"

    def getListeFiltre():
        annees = sorted(list(set([
            annee.year for annee in Serie.objects.all().values_list('date', flat=True).distinct()])), reverse=True)
        durees = {'< 15 min': (0, 15), '15min - 30min': (15, 30), '30min - 45min': (30, 45), '45min - 1h': (
            45, 60), '1h - 1h15': (60, 75), '1h15 - 1h30': (75, 90), '> 1h30': (90, 99999999)}
        genres = Serie.objects.values_list(
            'listGenre__nom', flat=True).distinct()
        return annees, durees, genres


class Role(models.Model):
    nom = models.CharField(max_length=100)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    acteur = models.ForeignKey(Personne, on_delete=models.CASCADE)

    def __str__(self):
        return f"Role : {self.acteur} --> {self.nom}"
