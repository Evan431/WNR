from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from appliWNR.models import Programme

User = get_user_model()

def index(request):
    return render(request, 'appliWNR/Accueil.html')

# def pageCreation(request):
#     form = UtilisateurInscription()
#     return render(request, 'appliWNR/pageCréation.html', { 'form' : form})

# def pageNonConnecte(request):
#     return render(request, 'appliWNR/page non connecte.html'), 


# ------------------------------------  Pour Creer un compte -----------------------------------#

def signup(request):
    if request.method == "POST":
        username = request.POST.get("Pseudo")
        password = request.POST.get("Mot_de_passe")
        email = request.POST.get("Adresse_mail")
        cgu = request.POST.get("caseCocher")  
        user = User.objects.create_user(username=username, password=password, email=email)
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
    return redirect(request, 'index')

# ------------------------------------  Pour supprimer un compte -----------------------------------#

def deleteAccount(request):
    return render(request, 'appliWNR/pageSuppressionCompte.html')

def confirmationSuppression(request):
    return render(request, 'appliWNR/confirmation suppression.html')


def resultatsRecherche(request):
    if request.method == "POST" :
        query = request.POST.get('Recherche', None)
        if query :
            results = Programme.objects.filter(titre__contains=query).values() | Programme.objects.filter(titreOriginal__icontains=query).values()
        return render(request, 'appliWNR/resultatsRecherche.html', {"results":results})
    return render(request, 'appliWNR/resultatsRecherche.html')

    #Potentielle solution avec Postgre (https://stackoverflow.com/questions/5619848/how-to-have-accent-insensitive-filter-in-django-with-postgres)

def statistiques(request):
    return render(request, 'appliWNR/statistiques.html')

def statistiquesGenerales(request):
    return render(request, 'appliWNR/statistiquesGenerales.html')

def programme(request):
    lettres = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    genres = ['Horreur','Fantastique','Science-fiction','Comédie','Romance','Drama']
    annees = ['2022','2003','2078']
    durees = ['2 h 30', '5 h', '1 h 45']
    #Postgre
    return render(request, 'appliWNR/programme.html', {"lettres":lettres, "genres":genres, "annees":annees, "durees":durees})

def compte(request):
    return render(request, 'appliWNR/compte.html')

def cgu(request):
    return render(request, 'appliWNR/cgu.html')

        