#!/usr/bin/python
# -*- coding: utf8 -*-
#
# PYDCC main program - User Interface
#


import config as CONFIG
import search
import bot
        
print("Pydcc")
print(" 1 : Rechercher")
print(" 2 : lancer le bot sur #barakuun")
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
        except:
                print("erreur searchAndParse")
        for ligne in resultats:
            print(ligne)
            
elif choix == 2 :
    bot = bot.Grabator();
    bot.start()
else:
        print(choix)

