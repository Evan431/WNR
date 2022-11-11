from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.shortcuts import redirect


class UtilisateurConnecte(models.Models):
    pseudo = models.fields.Charfiels(max_length=20)
    adresseMail = models.fields.EmailField(max_length=254)
    motDePase = models.fields.Charfiels(max_length=60) 
    recevoirMail = models.field.BooleanField()

class Utilisateur(models.Models):
    def seConnecter(pseudo, adresseMail, motDePAsse):
        user = User.objects.create_user('pseudo', 'adresseMail', 'motDePAsse')
        if user is not None:
            login(request, user)
            return True
        else:
            print('erreur lors de la connexion')
            return False 

    def seDeconnecter(user, request): # request est un objet HttpRequest
        if(verifierConnexion(user)==True){
            logout(request)
            return "l'utilisateur a été déconnecté"
        }
        return "Erreur, l'utilisateur n'est pas connecté"

    def verifierConnexion(user):
        if not request.user.is_authenticated:
            #redirection vers la page de connexion
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else
            return True

