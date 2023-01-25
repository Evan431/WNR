from script_recup_film import recupFilm
from script_recup_serie import recupSerie

listid = []


# fichier = open("movie.json", 'r', encoding="utf8")
fichier = open("tv_series.json", 'r', encoding="utf8")
lignes = fichier.readlines()
cpt = 0
for ligne in lignes:
    ligne = ligne.replace('\n', '')
    # ligne = ligne.split(',')[1].split(':')[1]
    ligne = ligne.split(',')[0].split(':')[1]
    listid.append(ligne)
    cpt += 1

for i in listid:
    # print("Film :", i, "récupéré")
    # recupFilm(i)
    print("Série :", i, "récupéré")
    recupSerie(i)


# exec(open('script_recup.py').read())
