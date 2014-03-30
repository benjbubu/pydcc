#!/usr/bin/python
#
# PYDCC main program - User Interface
#


import config as CONFIG
import search
        
print "Pydcc"
print " 1 : Rechercher"
print " 2 : Voir le DL en cours"
choix = input("Quel est votre choix?")

if choix == 1:
        query = raw_input("Indiquez votre recherche \n")
        html = search.search(query)
        resultats = search.parse(html)
        print(resultats)
        # print(html)
else:
        print(choix)

