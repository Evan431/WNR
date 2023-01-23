from script_recup_film import recupFilm

listid = []


fichier = open("movie.json", 'r', encoding="utf8")
lignes = fichier.readlines()
cpt = 0
for ligne in lignes:
    ligne = ligne.replace('\n', '')
    ligne = ligne.split(',')[1].split(':')[1]
    listid.append(ligne)
    if cpt >= 100:
        break
    cpt += 1

for i in listid:
    print("Film :", i, "récupéré")
    recupFilm(i)

# exec(open('script_recup.py').read())
