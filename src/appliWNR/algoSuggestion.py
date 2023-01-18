from collections import Counter
from appliWNR.models import *
from datetime import datetime, timedelta

#Fonction qui récupère, à partir d'une note donnée, tous les programmes qui ont cette note en utilisatent le Django ORM (Object-Relational Mapping)
def ChoixNote(note):
    ListProgramme = Note.objects.filter(note_isnull=False).values_list('programme', flat=True)
    return ListProgramme
    
#Fonction qui récupère, à partir d'un utilisateur, les 3 genres qui sont présents le plus de fois des  de films et séries qu'il a déjà vu
def GenrePlusFrequent(ListProgramme):
    ListeGenres = [genre for program in ListProgramme for genre in program.listGenre_set.all()]
    genre_counts = Counter(ListeGenres)
    most_common_genres = [genre for genre, count in genre_counts.most_common()] #on ne se sert pas du count 
    # most_common_genres = []
    # for genre, count in genre_counts.most_common():
    #     most_common_genres.append(genre)
    if len(most_common_genres) >=4 : 
        return most_common_genres[:3]
    elif len(most_common_genres) >=3 : 
        return most_common_genres[:2]
    elif len(most_common_genres) >=2 : 
        return most_common_genres[:1]
    else :
        return most_common_genres


#Fonction qui récupère, à partir d'un utilisateur et d'un métier, les 3 personnes qui sont présents le plus de fois des  de films et séries qu'il a déjà vu
def ActeurPlusFrequent(nomMetier, ListProgramme):
    ListePersonne= [Personne.metier for programme in ListProgramme for genre in programme.listPersonne_set.all() if Personne.metier == "nomMetier"]
    genre_counts = Counter(ListePersonne)
    most_common_personne = [personne for personne, count in genre_counts.most_common()] #on ne se sert pas du count 
    if len(most_common_personne) >=4 : 
        return most_common_personne[:3]
    elif len(most_common_personne) >=3 : 
        return most_common_personne[:2]
    elif len(most_common_personne) >=2 : 
        return most_common_personne[:1]
    else :
        return most_common_personne
#fonction qui retourne le pourcentage de chaque type de programme qu'un utilisateur a regardé
def typePrefere(ListProgramme):
    nombreSerie = 0
    nombreFilm = 0
    pourcentageSerie = 0
    pourcentageFilm = 0
    for programme in ListProgramme :
        if isinstance(programme, (Film)) :
            nombreFilm +=1
        if isinstance(programme, (Serie)) :
            nombreSerie +=1
    pourcentageSerie = nombreSerie * 100 / (nombreSerie + pourcentageFilm)
    pourcentageFilm = nombreFilm * 100 / (nombreSerie + pourcentageFilm)
    return pourcentageSerie, pourcentageFilm

def nombreOccurence(Liste, ListePref):
    count =0
    for i in Liste :
        if i in ListePref :
            count += 1
    return count

#vérifier la dernière date de mise à jour de la liste des suggestions
#return True si la dernière modification est il y a plus de 2h, sinon false 
def dateMiseJour():
    if format((datetime.now() - ListeSuggestion.derniereMAJ).seconds/3600) > 2 :
        return True
    else :
        return False

def choixProgramme(utilisateur, ListeSerie, ListeFilm, type):
    dicoTrieDecroissantFilm = dicoProgramme(utilisateur, ListeFilm)
    dicoTrieDecroissantSerie = dicoProgramme(utilisateur, ListeSerie)
    ListeSuggestion = []
    if type == "serie" :
        if len(dicoTrieDecroissantSerie) < 50 *0.75 :
            nombreSerie = len(dicoTrieDecroissantSerie)
            nombreFilm = len(dicoTrieDecroissantSerie)/3
        else :
            nombreSerie = 50*0.75
            nombreFilm = 50*0.25

        ListeSuggestion = [programme for programme in dicoTrieDecroissantSerie[:nombreSerie].keys()] 
        ListeSuggestion = [programme for programme in dicoTrieDecroissantFilm[:nombreFilm].keys()] 
        return ListeSuggestion

    elif type == "film":
        if len(dicoTrieDecroissantFilm) < 50 *0.75 :
            nombreSerie = len(dicoTrieDecroissantFilm)/3
            nombreFilm = len(dicoTrieDecroissantFilm)
        else :
            nombreSerie = 50*0.25
            nombreFilm = 50*0.75

        ListeSuggestion = [programme for programme in dicoTrieDecroissantFilm[:nombreFilm].keys()] 
        ListeSuggestion = [programme for programme in dicoTrieDecroissantSerie[:nombreSerie].keys()] 
        return ListeSuggestion  
    else :
        if len(dicoTrieDecroissantSerie) < 25  :
            nombreSerie = len(dicoTrieDecroissantSerie)
            nombreFilm = len(dicoTrieDecroissantSerie)
        elif len(dicoTrieDecroissantFilm) < 25  :
            nombreSerie = len(dicoTrieDecroissantFilm)
            nombreFilm = len(dicoTrieDecroissantFilm)
        else :
            nombreFilm = 25
            nombreSerie = 25
        ListeSuggestion = [programme for programme in dicoTrieDecroissantFilm[:nombreFilm].keys()] 
        ListeSuggestion = [programme for programme in dicoTrieDecroissantSerie[:nombreSerie].keys()] 
        return ListeSuggestion 

def dicoProgramme(utilisateur, Liste):
    ListeGenrePref = GenrePlusFrequent(utilisateur)
    ListeActeurPref = ActeurPlusFrequent(utilisateur, "acteur")
    ListeProducteurPref = ActeurPlusFrequent(utilisateur, "producteur")
    ListeCompaProdPref = ActeurPlusFrequent(utilisateur, "compagnies du production")
    ListeScenaristePref = ActeurPlusFrequent(utilisateur, "scenariste")
    scoreProgramme = {}
    for programme in Liste :
        for ListeGenres in Liste :
            score = nombreOccurence(ListeGenres, ListeGenrePref)

            ListeActeurs= [personne for personne in programme.listPersonne_set.all() if Personne.metier == "acteur"]
            score += nombreOccurence(ListeActeurs, ListeActeurPref)

            ListeScenaristes= [personne for personne in programme.listPersonne_set.all() if Personne.metier == "scénariste"]
            score += nombreOccurence(ListeScenaristes, ListeScenaristePref)

            ListeCompaProds= [personne for personne in programme.listPersonne_set.all() if Personne.metier == "compagnie de production"]
            score += nombreOccurence(ListeCompaProds, ListeCompaProdPref)

            ListeProducteurs= [personne for personne in programme.listPersonne_set.all() if Personne.metier == "producteurs"]
            score += nombreOccurence(ListeProducteurs, ListeProducteurPref)
                    
            scoreProgramme[programme]=score # Le score peut être entre 0 et 20

    return sorted(scoreProgramme.items(), key=lambda x: x[1], reverse=True)  
        
def algoSuggestion(utilisateur):
    if dateMiseJour() == True : 
        ListProgramme= ListeDejaVue.objects.get(utilisateur=utilisateur)
        pourcentageSerie, pourcentageFilm, = typePrefere(utilisateur)
        ListeProgTotal = Programme.objects.all() # enlever film et serie deja vue
        ListeFilm = []
        ListeSerie = []
        for programme in ListeProgTotal :
            if programme not in ListProgramme : 
                if isinstance(programme, (Film)) :
                    ListeFilm.append(programme)
                if isinstance(programme, (Serie)) :
                    ListeSerie.append(programme)

        if pourcentageSerie < 35 :
            return choixProgramme(utilisateur, ListeSerie, ListeFilm, Film)
        elif pourcentageFilm < 35 :
            return choixProgramme(utilisateur, ListeSerie, ListeFilm, Serie)
        else :
            return choixProgramme(utilisateur, ListeSerie, ListeFilm, "null")


    


           
    

