# Importation
from appliWNR.models import *
from tmdbv3api import TMDb, Movie, TV


# Configuration de l'API TMDB
tmdb = TMDb()
tmdb.api_key = '02a78ca3a58954b06e6011270b0be916'
tmdb.language = 'fr'
tmdb.debug = True


# RECUP FILM
# movie = Movie()
# id = 33196
# details = movie.details(id)

# production_companies = []
# for i in details.production_companies:
#     print(i)
#     production_companies.append(
#         CompagnieProduction.objects.get_or_create(nom=i['name'])[0])

# genres = []
# for i in details.genres:
#     genres.append(Genre.objects.get_or_create(nom=i['name'])[0])

# acteurs = {}
# for i in details.casts['cast'][0:10]:
#     name = i['name'].split(" ")
#     acteurs[Personne.objects.get_or_create(
#         nom=" ".join(name[1:]), prenom=name[0], metier="acteur")[0]] = i['character']

# personnes = []
# for p in details.casts['crew']:
#     if p['job'] == "Producer":
#         name = p['name'].split(" ")
#         personnes.append(Personne.objects.get_or_create(
#             prenom=name[0], nom=" ".join(name[1:]), metier="producteur")[0])

# film = Film.objects.get_or_create(titre=details.title, titreOriginal=details.original_title,
#                                   popularite=details.popularity, description=details.overview, date=details.release_date, affiche=details.poster_path, duree=details.runtime, bandeAnnonce=details.video)[0]

# for i in production_companies:
#     film.listCompaProd.add(i)

# for i in genres:
#     film.listGenre.add(i)

# for k, v in acteurs.items():
#     film.listPersonne.add(k)
#     Role.objects.get_or_create(nom=v, programme=film, acteur=k)[0]

# for i in personnes:
#     film.listPersonne.add(i)
# film.save()


# RECUP SERIE
tv = TV()
id = 66732
details = tv.details(id)
production_companies = []
for i in details.production_companies:
    print(i)
    production_companies.append(
        CompagnieProduction.objects.get_or_create(nom=i['name'])[0])

genres = []
for i in details.genres:
    genres.append(Genre.objects.get_or_create(nom=i['name'])[0])

acteurs = {}
for i in details.credits['cast'][0:10]:
    name = i['name'].split(" ")
    acteurs[Personne.objects.get_or_create(
        nom=" ".join(name[1:]), prenom=name[0], metier="acteur")[0]] = i['character']

personnes = []
for p in details.credits['crew']:
    if p['job'] == "Producer":
        name = p['name'].split(" ")
        personnes.append(Personne.objects.get_or_create(
            prenom=name[0], nom=" ".join(name[1:]), metier="producteur")[0])

tv = Serie.objects.get_or_create(titre=details.name, titreOriginal=details.original_name,
                                 popularite=details.popularity, description=details.overview, date=details.first_air_date, affiche=details.poster_path, dureeMoyEp=details.episode_run_time[0], bandeAnnonce=details.videos['results'][0]['key'], nombreSaison=details.number_of_seasons, nombreEpisodes=details.number_of_episodes, status=details.status)[0]

for i in production_companies:
    tv.listCompaProd.add(i)

for i in genres:
    tv.listGenre.add(i)

for k, v in acteurs.items():
    tv.listPersonne.add(k)
    Role.objects.get_or_create(nom=v, programme=tv, acteur=k)[0]

for i in personnes:
    tv.listPersonne.add(i)
tv.save()
