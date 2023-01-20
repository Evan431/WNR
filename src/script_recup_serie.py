# Importation
from appliWNR.models import *
from tmdbv3api import TMDb, TV

# Configuration de l'API TMDB
tmdb = TMDb()
tmdb.api_key = '02a78ca3a58954b06e6011270b0be916'
tmdb.language = 'fr'
tmdb.debug = False


tv = TV()
id = 93405
details = tv.details(id)
production_companies = []
for i in details.production_companies:
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

plateformes = []
watch_provider = tv.watch_providers(id)
for i in watch_provider.results['FR']['flatrate']:
    if i.provider_name != 'Netflix basic with Ads':
        plateformes.append(
            Plateforme.objects.get_or_create(nom=i.provider_name)[0])

runtime = details.episode_run_time[0] if len(
    details.episode_run_time) > 0 else 0

serie = Serie.objects.get_or_create(titre=details.name, titreOriginal=details.original_name,
                                    popularite=details.popularity, description=details.overview, date=details.first_air_date, affiche=details.poster_path, dureeMoyEp=runtime, bandeAnnonce=details.videos['results'][0]['key'], nombreSaison=details.number_of_seasons, nombreEpisodes=details.number_of_episodes, status=details.status)[0]

for i in production_companies:
    serie.listCompaProd.add(i)

for i in plateformes:
    serie.listPlateforme.add(i)

for i in genres:
    serie.listGenre.add(i)

for k, v in acteurs.items():
    serie.listPersonne.add(k)
    Role.objects.get_or_create(nom=v, programme=serie, acteur=k)[0]

for i in personnes:
    serie.listPersonne.add(i)
serie.save()


# exec(open('script_recup_serie.py').read())
