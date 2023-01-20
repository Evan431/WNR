# Importation
from appliWNR.models import *
from tmdbv3api import TMDb, Movie, TV


# Configuration de l'API TMDB
tmdb = TMDb()
tmdb.api_key = '02a78ca3a58954b06e6011270b0be916'
tmdb.language = 'fr'
tmdb.debug = True


# RECUP FILM
movie = Movie()
id = 333339
details = movie.details(id)

production_companies = []
for i in details.production_companies:
    production_companies.append(
        CompagnieProduction.objects.get_or_create(nom=i['name'])[0])

genres = []
for i in details.genres:
    genres.append(Genre.objects.get_or_create(nom=i['name'])[0])

acteurs = {}
for i in details.casts['cast'][0:10]:
    name = i['name'].split(" ")
    acteurs[Personne.objects.get_or_create(
        nom=" ".join(name[1:]), prenom=name[0], metier="acteur")[0]] = i['character']

personnes = []
for p in details.casts['crew']:
    if p['job'] == "Producer":
        name = p['name'].split(" ")
        personnes.append(Personne.objects.get_or_create(
            prenom=name[0], nom=" ".join(name[1:]), metier="producteur")[0])

plateformes = []
watch_provider = movie.watch_providers(id)

for i in watch_provider.results['FR']['flatrate']:
    if i.provider_name != 'Netflix basic with Ads':
        plateformes.append(
            Plateforme.objects.get_or_create(nom=i.provider_name)[0])

film = Film.objects.get_or_create(titre=details.title, titreOriginal=details.original_title,
                                  popularite=details.popularity, description=details.overview, date=details.release_date, affiche=details.poster_path, duree=details.runtime, bandeAnnonce=details.video)[0]

for i in production_companies:
    film.listCompaProd.add(i)

for i in genres:
    film.listGenre.add(i)

for k, v in acteurs.items():
    film.listPersonne.add(k)
    Role.objects.get_or_create(nom=v, programme=film, acteur=k)[0]

for i in personnes:
    film.listPersonne.add(i)

for i in plateformes:
    film.listPlateforme.add(i)
film.save()

# exec(open('script_recup_film.py').read())
