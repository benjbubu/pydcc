#!/usr/bin/python
#
# PYDCC main program - User Interface
#


import config as CONFIG
import search
        
print("Pydcc")
print(" 1 : Rechercher")
print(" 2 : Voir le DL en cours")
try:
        choix = input("Quel est votre choix?\n")
        choix = int(choix)
except:
        print("erreur saisie/conversion choix")

if choix == 1 :
        try:
                query = input("Indiquez votre recherche \n")
        except:
                print("erreur input recherche")
        try:
                resultats = search.searchAndParse(query)
                print(resultats)
        except:
                print("erreur searchAndParse")
else:
        print(choix)

