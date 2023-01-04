from django.http import HttpResponse
from django.shortcuts import render, redirect
from appliWNR.forms.creationCompte import UtilisateurInscription, CreateUtilisateur
from django.contrib.auth import authenticate, login
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def index(request):
    return render(request, 'appliWNR/Accueil.html')

# def pageCreation(request):
#     form = UtilisateurInscription()
#     return render(request, 'appliWNR/pageCréation.html', { 'form' : form})

# def pageNonConnecte(request):
#     return render(request, 'appliWNR/page non connecte.html'), 

def signup_page(request):
    form = UtilisateurInscription()
    if request.method == 'GET':
        form = UtilisateurInscription(request.GET)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Le compte a bien été créé')
            login(request, user)
            return redirect('appliWNR/pageConnexion.html')
        else :
            form = UtilisateurInscription()
    return render(request, 'appliWNR/pageInscription.html', {'form': form})

def register(request):
    form = UtilisateurInscription()
    if request.method == "POST":
        form = UtilisateurInscription(request.POST)
        if form.is_valid(): 
            form.save()
            messages.success(request, 'Le compte a bien été créé')
            user = form.cleaned_data.get()
            return redirect('appliWNR/pageConnexion.html')
    else :
        form = UtilisateurInscription()
    return render(request, 'appliWNR/pageInscription.html', { 'form' : form})

# Pour se connecter
def login_page(request):
    form = CreateUtilisateur()
    message = ''
    if request.method == 'GET':
        form = CreateUtilisateur(request.GET)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides.'
    return render(request, 'appliWNR/pageConnexion.html', context={'form': form, 'message': message})

def login(request):
    if request.method == "POST":
        pseudo = request.POST.get('pseudo')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = authenticate(request, pseudo=pseudo, password=password, email=email)
        if user is not None:
            login(request, pseudo)
            return redirect('index')
        else :
            messages.info(request, 'Mot de passe ou email invalide')

    return render(request, 'appliWNR/page non connecte.html'), 

        