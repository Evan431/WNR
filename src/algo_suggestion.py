from collections import Counter
from appliWNR.models import *
from datetime import datetime

# Fonction qui récupère, à partir d'une note donnée, tous les programmes qui ont cette note en utilisatent le Django ORM (Object-Relational Mapping)
# FIXME


def ChoixNote(note):
    ListProgramme = Note.objects.filter(
        note_isnull=False).values_list('programme', flat=True)
    return ListProgramme


# Fonction qui récupère les 3 genres présents le plus de fois dans la liste de programme déjà vue d'un utilisateur
def GenrePlusFrequent(utilisateur):
    listeProgramme, _ = ListeDejaVue.objects.get_or_create(
        utilisateur=utilisateur)
    listeGenres = list(set([
        genre for program in listeProgramme.programmes.all() for genre in program.listGenre.all()]))
    genresFrequent = [genre for genre, _ in Counter(listeGenres).most_common()]
    # most_common_genres = []
    # for genre, count in genre_counts.most_common():
    #     most_common_genres.append(genre)
    return genresFrequent[:3] if len(genresFrequent) >= 4 else genresFrequent[:(len(genresFrequent)-1)]


# Fonction qui récupère les 3 personnes présents le plus de fois dans la liste de programme déjà vue d'un utilisateur
def ActeurPlusFrequent(utilisateur, nomMetier):
    listeProgramme, _ = ListeDejaVue.objects.get_or_create(
        utilisateur=utilisateur)
    listePersonne = [personne for programme in listeProgramme.programmes.all() for personne in programme.listPersonne.all(
    ) if personne.metier == nomMetier]
    personnesFrequente = [personne for personne,
                          _ in Counter(listePersonne).most_common()]
    return personnesFrequente[:3] if len(personnesFrequente) >= 4 else personnesFrequente[:(len(personnesFrequente)-1)]


# Fonction qui retourne la répartition (en %) du type de programme qu'un utilisateur a regardé
def typePrefere(utilisateur):
    listeProgramme, _ = ListeDejaVue.objects.get_or_create(
        utilisateur=utilisateur)
    nbSerie, nbFilm = 0, 0
    for programme in listeProgramme.programmes.all():
        print(programme)
        if isinstance(programme, (Film)):
            nbFilm += 1
        elif isinstance(programme, (Serie)):
            nbSerie += 1

    if nbFilm + nbSerie == 0:
        return 50, 50
    return nbSerie * 100 / (nbSerie + nbFilm), nbFilm * 100 / (nbSerie + nbFilm)


def nbPointCommun(liste, listePref):
    count = 0
    for i in liste:
        if i in listePref:
            count += 1
    return count


# Calcul le score de chaque programme (1 point par point commun)
def dicoProgramme(utilisateur, liste):
    listeGenrePref = GenrePlusFrequent(utilisateur)
    listeActeurPref = ActeurPlusFrequent(utilisateur, "acteur")
    listeProducteurPref = ActeurPlusFrequent(utilisateur, "producteur")
    listeCompaProdPref = ActeurPlusFrequent(
        utilisateur, "compagnies du production")
    # listeScenaristePref = ActeurPlusFrequent(utilisateur, "scenariste")
    scoreProgramme = {}
    for programme in liste:
        listeGenres = [genre for genre in programme.listGenre.all()]
        score = nbPointCommun(listeGenres, listeGenrePref)

        listeActeurs = [personne for personne in programme.listPersonne.all(
        ) if Personne.metier == "acteur"]
        score += nbPointCommun(listeActeurs, listeActeurPref)

        # ListeScenaristes = [personne for personne in programme.listPersonne.all() if Personne.metier == "scénariste"]
        # score += nbPointCommun(ListeScenaristes, listeScenaristePref)

        listeCompaProds = [compa for compa in programme.listCompaProd.all()]
        score += nbPointCommun(listeCompaProds, listeCompaProdPref)

        listeProducteurs = [personne for personne in programme.listPersonne.all(
        ) if Personne.metier == "producteurs"]
        score += nbPointCommun(listeProducteurs, listeProducteurPref)

        # Le score peut être entre 0 et 20
        scoreProgramme[programme] = score
    print(scoreProgramme)
    return sorted(scoreProgramme.items(), key=lambda x: x[1], reverse=True)


def calculRepartitionSuggestion(dicoProgramme):
    if len(dicoProgramme) < 50 * 0.75:
        nbType1 = len(dicoProgramme)
        nbType2 = len(dicoProgramme)/3
    else:
        nbType1 = 50*0.75
        nbType2 = 50*0.25
    return nbType1, nbType2


def choixProgramme(utilisateur, listeSerie, listeFilm, type):
    dicoTrieDecroissantFilm = dicoProgramme(utilisateur, listeFilm)
    dicoTrieDecroissantSerie = dicoProgramme(utilisateur, listeSerie)

    if type not in ["film", "serie"]:
        nombreSerie, nombreFilm = calculRepartitionSuggestion(
            dicoTrieDecroissantFilm) if type == "film" else calculRepartitionSuggestion(dicoTrieDecroissantSerie)
    else:
        if len(dicoTrieDecroissantSerie) <= 25:
            nombreSerie = len(dicoTrieDecroissantSerie)
            nombreFilm = 50 - len(dicoTrieDecroissantSerie)
        elif len(dicoTrieDecroissantFilm) < 25:
            nombreSerie = 50 - len(dicoTrieDecroissantFilm)
            nombreFilm = len(dicoTrieDecroissantFilm)
    return dicoTrieDecroissantFilm[:int(nombreFilm)] + dicoTrieDecroissantSerie[:int(nombreSerie)]


def algoSuggestion(utilisateur):
    listProgramme = ListeDejaVue.objects.get(utilisateur=utilisateur)
    pourcentageSerie, pourcentageFilm, = typePrefere(utilisateur)
    listeFilm, listeSerie = [], []
    for programme in Programme.objects.all():
        if programme not in listProgramme.programmes.all():
            if Film.objects.filter(id=programme.id).exists():
                listeFilm.append(programme)
            if Serie.objects.filter(id=programme.id).exists():
                listeSerie.append(programme)
    if pourcentageSerie < 35:
        remplirListeSuggestion(choixProgramme(
            utilisateur, listeSerie, listeFilm, "film"), utilisateur)
    elif pourcentageFilm < 35:
        remplirListeSuggestion(choixProgramme(
            utilisateur, listeSerie, listeFilm, "serie"), utilisateur)
    else:
        remplirListeSuggestion(choixProgramme(
            utilisateur, listeSerie, listeFilm, "null"), utilisateur)


def remplirListeSuggestion(liste, user):
    listeUser, _ = ListeSuggestion.objects.get_or_create(utilisateur=user)
    listeUser.clean()
    liste.sort(key=lambda x: x[1])
    liste.reverse()
    for programme in liste:
        print("fin", programme)
        listeUser.programmes.add(programme[0])
    listeUser.save()


# Ajout possible : varier score avec note contenu et/ou popularité
