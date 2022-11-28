from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'appliWNR/Accueil.html')

def pageCreation(request):
    return render(request, 'appliWNR/pageCréation.html')

def pageNonConnecte(request):
    return render(request, 'appliWNR/page non connecte.html')

def resultatsRecherche(request):
    return render(request, 'appliWNR/resultatsRecherche.html')