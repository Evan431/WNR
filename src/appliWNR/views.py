from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.core.mail import send_mail
from django.template.defaultfilters import date
from django.db.models import Q


import random
from appliWNR.models import *

User = get_user_model()


def index(request):
    user = request.user
    films = Film.objects.all()[:10]
    series = Serie.objects.all()[:10]
    tendances = Programme.objects.order_by('-popularite')[:10]
    if user.is_anonymous:
        maListe, suggestion = False, False
    else:
        maListe = MaListe.objects.get_or_create(
            utilisateur=user)[0].programmes.all()[:10]
        suggestion = ListeSuggestion.objects.get_or_create(
            utilisateur=user)[0].programmes.all()[:10]

    # programmes = Programme.objects.all()[:10]
    return render(request, 'appliWNR/accueil.html', {"suggestion": suggestion, "maListe": maListe, "films": films, "series": series, "tendances": tendances})

# ------------------------------------  Pour Creer un compte -------------------"----------------#


def signup(request):
    # TODO Verif checkbox CGU
    if request.method == "POST":
        username = request.POST.get("Pseudo")
        password = request.POST.get("Mot_de_passe")
        email = request.POST.get("Adresse_mail")
        cgu = request.POST.get("caseCocher")
        user = User.objects.create_user(
            username=username, password=password, email=email)
        login(request, user)
        return redirect('index')

    return render(request, 'appliWNR/pageInscription.html')

# ------------------------------------  Pour se connecter -----------------------------------#


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("Pseudo")
        password = request.POST.get("Mot_de_passe")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'appliWNR/pageConnexion.html')

# ------------------------------------  Pour se deconnecter -----------------------------------#


def logout_request(request):
    logout(request)
    return redirect('index')

# ------------------------------------  Pour supprimer un compte -----------------------------------#


def deleteAccount(request):
    return render(request, 'appliWNR/pageSuppressionCompte.html')


def confirmationSuppression(request):
    user = request.user
    user.delete()
    return render(request, 'appliWNR/confirmation suppression.html')


def resultatsRecherche(request):
    if request.method == "POST":
        query = request.POST.get('Recherche', None)
        if query:
            results = Programme.objects.filter(titre__icontains=query).values(
            ) | Programme.objects.filter(titreOriginal__icontains=query).values()
        autocompletion = query
        return render(request, 'appliWNR/resultatsRecherche.html', {"results": results, "autocompletion": autocompletion})
    return render(request, 'appliWNR/resultatsRecherche.html')

    # Potentielle solution avec Postgre (https://stackoverflow.com/questions/5619848/how-to-have-accent-insensitive-filter-in-django-with-postgres)


def statistiques(request):
    return render(request, 'appliWNR/statistiques.html')


def statistiquesGenerales(request):
    return render(request, 'appliWNR/statistiquesGenerales.html')


def programme(request, type):
    annee, lettre, genre, duree = "", "", "", ""
    lettres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    if type == 'film':
        annees, durees, genres = Film.getListeFiltre()
    elif type == 'serie':
        annees, durees, genres = Serie.getListeFiltre()

    if request.method == "POST":
        annee = request.POST.get("annee")
        lettre = request.POST.get("lettre")
        genre = request.POST.get("genre")
        duree = request.POST.get("duree")
        query = Q()

        if annee:
            query = query & Q(date__year=annee)
        if lettre:
            query = query & (Q(titre__startswith=lettre) |
                             Q(titreOriginal__startswith=lettre))
        if genre:
            query = query & Q(listGenre__nom=genre)

        if type == 'film':
            if duree:
                duree = durees[request.POST.get("duree")]
                query = query & Q(duree__gte=duree[0], duree__lte=duree[1])
            programmes = Film.objects.filter(query)[:50]

        elif type == 'serie':
            if duree:
                duree = durees[request.POST.get("duree")]
                query = query & Q(
                    dureeMoyEp__gte=duree[0], dureeMoyEp__lte=duree[1])
            programmes = Serie.objects.filter(query)[:50]
        else:
            programmes = Programme.objects.all()[:50]
        duree = request.POST.get("duree")
    else:
        programmes = Serie.objects.all(
        ) if type == 'serie' else Film.objects.all()[:50]
    return render(request, 'appliWNR/programme.html', {"lettres": lettres, "genres": genres, "annees": annees, "durees": durees, "programmes": programmes, "type": type, "genre": genre, "annee": annee, "lettre": lettre, "duree": duree})


def compte(request):
    listeDejaVue, _ = ListeDejaVue.objects.get_or_create(
        utilisateur=request.user)
    return render(request, 'appliWNR/compte.html', {"listeDejaVue": listeDejaVue.programmes.all()})


def cgu(request):
    return render(request, 'appliWNR/cgu.html')


def detail_programme(request, id):
    exists = Film.objects.filter(id=id).exists()
    if exists:
        programme = Film.objects.get(id=id)
    else:
        programme = get_object_or_404(Serie, id=id)

    isFilm = True if isinstance(programme, Film) else False
    producteurs = programme.listPersonne.filter(metier="producteur").all()
    compaProd = programme.listCompaProd.all()
    plateformes = ["/images/"+x.nom.lower().replace(" ", "_")+".svg"
                   for x in programme.listPlateforme.all()]
    print(plateformes)

    acteurs = {}
    for acteur in programme.listPersonne.filter(metier="acteur"):
        acteurs[acteur] = get_object_or_404(
            Role, programme=programme, acteur=acteur)
    scenaristes = programme.listPersonne.filter(metier="scenariste").all()

    # Test si programme dans listes
    user = request.user
    if user.is_anonymous:
        inMaListe, inListeDejaVue = False, False
    else:
        p = get_object_or_404(Programme, id=id)
        maListe, _ = MaListe.objects.get_or_create(
            utilisateur=user)
        inMaListe = True if p in maListe.programmes.all() else False
        listeDejaVue, _ = ListeDejaVue.objects.get_or_create(
            utilisateur=user)
        inListeDejaVue = True if p in listeDejaVue.programmes.all() else False

    return render(request, 'appliWNR/detail_programme.html', {"programme": programme, "isFilm": isFilm, "producteurs": producteurs, "scenaristes": scenaristes, "acteurs": acteurs, "compaProd": compaProd, "inListeDejaVue": inListeDejaVue, "inMaListe": inMaListe, "user": user, "plateformes": plateformes})


def noteProgramme(request, id, note):
    programme = get_object_or_404(Programme, id=id)
    user = request.user
    if user.is_anonymous:
        return render(request, 'appliWNR/pageConnexion.html')
    else:
        user.noterProgramme(programme, note)
    programme.majNote()
    return redirect('detail_programme', id=id)


def listProgramme(request, id, typeListe, action):
    programme = get_object_or_404(Programme, id=id)
    user = request.user
    if typeListe == 'maListe':
        liste, _ = MaListe.objects.get_or_create(utilisateur=user)
    elif typeListe == 'listeDejaVue':
        liste, _ = ListeDejaVue.objects.get_or_create(utilisateur=user)

    if action == 'add' and programme not in liste.programmes.all():
        liste.programmes.add(programme)
    elif action == 'remove' and programme in liste.programmes.all():
        liste.programmes.remove(programme)

    liste.save()
    return redirect('detail_programme', id=id)


def liste(request, typeListe):
    user = request.user
    if typeListe == 'maListe':
        liste, _ = MaListe.objects.get_or_create(utilisateur=user)
        nomListe = "Ma liste"
    elif typeListe == 'listeDejaVue':
        liste, _ = ListeDejaVue.objects.get_or_create(utilisateur=user)
        nomListe = "Déjà vue"
    elif typeListe == 'listeSuggestion':
        liste, _ = ListeSuggestion.objects.get_or_create(utilisateur=user)
        nomListe = "Suggestion"

    return render(request, 'appliWNR/liste.html', {"programmes": liste.programmes.all, "nomListe": nomListe})
