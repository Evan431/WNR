from django.test import TestCase
from appliWNR.models import Film

# Create your tests here.

class URLTests(TestCase):
    def test_pageAccueil(self):
        response = self.client.post('/')
        self.assertEqual(response.status_code, 200)

    def test_pageCgu(self):
        response = self.client.post('cgu/')
        self.assertEqual(response.status_code, 200)

    def test_pageCompte(self):
        response = self.client.post('compte/')
        self.assertEqual(response.status_code, 200)

    def test_pageConfirmationSuppression(self):
        response = self.client.post('pageConfirmationSuppression/')
        self.assertEqual(response.status_code, 200)

    def test_pageConnexion(self):
        response = self.client.post('pageConnexion/')
        self.assertEqual(response.status_code, 200)

    def test_pageInscription(self):
        response = self.client.post('pageInscription/')
        self.assertEqual(response.status_code, 200)

    def test_pageSuppression(self):
        response = self.client.post('pageSuppresionCompte/')
        self.assertEqual(response.status_code, 200)
    
    def test_pageProgramme(self):
        response = self.client.post('programme/')
        self.assertEqual(response.status_code, 200)
    
    def test_pageStatistiques(self):
        response = self.client.post('statistiques/')
        self.assertEqual(response.status_code, 200)

    def test_pageStatistiquesGenerales(self):
        response = self.client.post('statistiquesGenerales/')
        self.assertEqual(response.status_code, 200)

    def test_pageResultatsRecherche(self):
        response = self.client.post('resultatsRecherche/')
        self.assertEqual(response.status_code, 200)
    
    def test_pageDeconnexion(self):
        response = self.client.post('deconnexion/')
        self.assertEqual(response.status_code, 200)

class TestFilm(TestCase):

    def setUp(self):
        self.film1 =  Film.objects.create(id=1, original_title='Film 1', overview='Film 1 Overview', poster_path='poster1.jpg', production_companies='Company 1')
        self.film2 = Film.objects.create(id=2, original_title='Film 2', overview='Film 2 Overview', poster_path='poster2.jpg', production_companies='Company 2')

    def test_film_original_title(self):
        self.assertEqual(self.film1.original_title, 'Film 1')
        self.assertEqual(self.film2.original_title, 'Film 2')
    
    def test_film_overview(self):
        self.assertEqual(self.film1.overview, 'Film 1 Overview')
        self.assertEqual(self.film2.overview, 'Film 2 Overview')
    
    def test_film_poster_path(self):
        self.assertEqual(self.film1.poster_path, 'poster1.jpg')
        self.assertEqual(self.film2.poster_path, 'poster2.jpg')
    
    def test_film_production_companies(self):
        self.assertEqual(self.film1.production_companies, 'Company 1')
        self.assertEqual(film2.production_companies, 'Company 2')

    
