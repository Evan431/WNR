from django.http import HttpResponse
from django.shortcuts import render
from appliWNR.models.programme import Programme

def index(request):
    return render(request, 'appliWNR/Accueil.html')

def pageCreation(request):
    return render(request, 'appliWNR/pageCréation.html')

def pageNonConnecte(request):
    return render(request, 'appliWNR/page non connecte.html')

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