from django.test import TestCase

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


    
