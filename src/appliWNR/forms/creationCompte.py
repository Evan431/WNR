from django import forms
from appliWNR.models import Utilisateur
from django.contrib.auth.forms import UserCreationForm

class UtilisateurInscription(forms.Form):
    class Meta(UserCreationForm.Meta):#indiquer quel model utiliser pour utiliser le formulaire
        model = Utilisateur
        fields =['pseudo', 'adresseMail', 'motDePase', 'cgu']
        # widgets = {
        #     'pseudo': forms.TextInput(attrs={"placeholder": "Pseudo"}),
        #     'adresseMail': forms.EmailField(attrs={ "placeholder": "Adresse mail"}),
        #     'motDePase': forms.PasswordInput(attrs={ "placeholder": "mot de passe"}),
        #     'cgu': forms.CheckboxInput(attrs={"class": "caseCocher"})        
        # }

class CreateUtilisateur(forms.Form):
    class Meta:
        email = forms.EmailField(max_length=254, label='email')
        password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')

