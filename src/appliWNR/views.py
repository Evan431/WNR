from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.core.mail import send_mail
from django.template.defaultfilters import date
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


import random
from appliWNR.models import *

User = get_user_model()


def index(request):
    programmes = Programme.objects.all()[:10]
    return render(request, 'appliWNR/Accueil.html', {"programmes": programmes})

# ------------------------------------  Pour Creer un compte -------------------"----------------#


def signup(request):
    # TODO Verif checkbox CGU
    if request.method == "POST":
        username = request.POST.get("Pseudo")
        password = request.POST.get("Mot_de_passe")
        email = request.POST.get("Adresse_mail")
        cgu = request.POST.get("caseCocher")

        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError as e:
            messages.error(request, "L'adresse email n'est pas valide");
            return redirect('signup')

        user = User.objects.create_user(
            username=username, password=password, email=email)
        login(request, user)

        # Generate verification code

        code = urlsafe_base64_encode(force_bytes(user.pk))

        # Render email template

        subject = 'confirmation de votre inscription'
        message = render_to_string('/home/vigaborit/Programmation/SAE301/projetWNR/WNR/src/appliWNR/templates/appliWNR/email_verification.txt', {'code' : code, 'user' : user})
        from_email = 'gaboritvictor13@gmail.com'
        recipient_list = [user.email]

        # Send email

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, "Un email de verification à été envoyer à l'adresse email saisie")

        return redirect('index')

    return render(request, 'appliWNR/pageInscription.html')
# ------------------------------------  Pour verifier l'email -----------------------------------#

def verify_email(request, code):
    try:
        # Decode the code and get the user id
        user_id = force_str(urlsafe_base64_decode(code))
        #user = User.objects.get(pk=user_id)
        user = request.user
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and not user.is_active:
        user.is_active = True
        user.save()
        messages.success(request, "Votre compte a été activé avec succès.")
        return redirect('login')
    else:
        messages.error(request, "Le lien de vérification n'est pas valide.")
        return redirect('index')

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
    lettres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    genres = [genre for genre in Genre.objects.all()]
    annees = [annee
              for annee in Programme.objects.all().values_list('date')]
    durees = ['< 30 min', '30min - 1h', '1h - 1h30',
              '1h30 - 2h', '2h - 2h30', '2h30 - 3h', '> 3h']

    if type == 'film':
        if request.method == "POST":
            annee = request.POST.get("annee")
            lettre = request.POST.get("lettre")
            genre = Genre.objects.get_or_create(
                nom=request.POST.get("genre"))
            # programmes = Film.objects.filter(date=annee)
            # programmes = Film.objects.filter(titre__startswith=lettre) | Film.objects.filter(titreOriginal__startswith=lettre)
            programmes = Film.objects.filter(listGenre=genre)

        else:
            programmes = Film.objects.all()
    elif type == 'serie':
        programmes = Serie.objects.all()
    # Postgre
    return render(request, 'appliWNR/programme.html', {"lettres": lettres, "genres": genres, "annees": annees, "durees": durees, "programmes": programmes})


def compte(request):

    listeDejaVue = request.user.getListeDejaVue(
    ).programmes.all()
    return render(request, 'appliWNR/compte.html', {"listeDejaVue": listeDejaVue})


def cgu(request):
    return render(request, 'appliWNR/cgu.html')


def detail_programme(request, id):
    exists = Film.objects.filter(id=id).exists()
    if exists:
        programme = Film.objects.get(id=id)
    else:
        programme = get_object_or_404(Serie, id=id)

    isFilm = True if isinstance(programme, Film) else False
    producteurs = programme.listPersonne.filter(metier="producteur").all

    acteurs = {}
    for acteur in programme.listPersonne.filter(metier="acteur"):
        acteurs[acteur] = get_object_or_404(
            Role, programme=programme, acteur=acteur)
    scenaristes = programme.listPersonne.filter(metier="scenariste").all

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

    return render(request, 'appliWNR/detail_programme.html', {"programme": programme, "isFilm": isFilm, "producteurs": producteurs, "scenaristes": scenaristes, "acteurs": acteurs, "inListeDejaVue": inListeDejaVue, "inMaListe": inMaListe, "user": user})


def noteProgramme(request, id, note):
    # BUG : probleme
    programme = get_object_or_404(Programme, id=id)
    user = request.user
    user.noterProgramme(programme, note)
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
    elif typeListe == 'listeDejaVue':
        liste, _ = ListeDejaVue.objects.get_or_create(utilisateur=user)
    return render(request, 'appliWNR/liste.html', {"programmes": liste.programmes.all})
