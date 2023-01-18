from django.test import TestCase
from appliWNR.models import *

#ajout de quelques test pour le model

class TestModel(TestCase):
    # Objet en commun dans plusieurs fonctions 

    person1 = Personne.objects.create(nom='DiCaprio', prenom='Leonardo ', metier='Actor')
    person2 = Personne.objects.create(nom='Cameron', prenom='James ', metier='Director')

    genre1 = Genre.objects.create(nom='Action')
    genre2 = Genre.objects.create(nom='Comédie')

    compaProd1 = CompagnieProduction.objects.create(nom='American International Pictures')
    compaProd2 = CompagnieProduction.objects.create(nom='Gonella Production')

    def TestCompaProd(self):
        self.assertEqual(self.compaProd1.nom, 'American International Pictures')
        self.assertEqual(self.compaProd2.nom, 'Gonella Production')

    def TestPersonne(self):
        self.assertEqual(self.person1.nom, 'DiCaprio')
        self.assertEqual(self.person1.prenom, 'Leonardo')
        self.assertEqual(self.person1.metier, 'Actor')
        self.assertEqual(self.person2.nom, 'Cameron')
        self.assertEqual(self.person2.prenom, 'James')
        self.assertEqual(self.person2.metier, 'Director')

    def TestGenre(self):    
        self.assertEqual(self.genre1.nom, "Action")
        self.assertEqual(self.genre2.nom, "Comédie")

    def TestProgramme(self): 
        programme1 = Programme.objects.create(titre='Avatar', titreOriginal='Avatar', bandeAnnonce='https://youtu.be/O1CzgULNRGs', popularite=4.2, affiche='avatar.png', note_global=8.5, 
                                              description="Le personnage central de l'histoire, Jake Sully, un marine paraplégique doté d'un avatar ...", date='2009-12-16')
        programme1.listPersonne.add(self.person1, self.person2)
        programme1.listGenre.add(self.genre1, self.genre2)
        programme1.listCompaProd.add(self.compaProd1)
        programme2 = Programme.objects.create(titre='Avatar 2', titreOriginal='Avatar 2', bandeAnnonce='https://youtu.be/5uSCcKyR-eQ', popularite=4.8, affiche='avatar2.png', note_global=9, 
                                              description="Se déroulant plus d'une décennie après les événements relatés dans le premier film, ce 2e film raconte ...", date='2022-12-14')
        programme2.listPersonne.add(self.person1)
        programme2.listGenre.add(self.genre1)
        programme2.listCompaProd.add(self.compaProd2)

        #Quelques vérifications  
        self.assertEqual(programme1.titre, "Avatar")
        self.assertEqual(programme2.titre, "Avatar 2")
        self.assertEqual(programme1.popularite, 4.2)
        self.assertEqual(programme2.popularite, 4.8)

    def TestUtiliateur(self): 
        utilisateur1 = Utilisateur.objects.create_user(username='labrette', password='1234')
        utilisateur2 = Utilisateur.objects.create_user(username='jucarvalh', password='5678')

        self.assertEqual(utilisateur1.nom, "labrette")
        self.assertEqual(utilisateur2.nom, "jucarvalh")
        self.assertEqual(utilisateur1.password, "1234")
        self.assertEqual(utilisateur2.password, "5678")
