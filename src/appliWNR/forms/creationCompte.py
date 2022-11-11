from django import forms

class Connexion(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    