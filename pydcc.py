#!/usr/bin/python
# -*- coding: utf8 -*-
#
# PYDCC main program - User Interface
#

from config import *
import search
import bot
        
print("Pydcc")
print(" 1 : Rechercher")
print(" 2 : lancer le bot pour test sur abjects")
print(" 3 : lancer le bot sur #barakuun")

try:
    choix = input("Quel est votre choix?\n")
    choix = int(choix)
except:
    print("pydcc.py : erreur saisie/conversion choix")

if choix == 1 :
    try:
        query = input("Indiquez votre recherche \n")
    except:
        print("pydcc.py : erreur input recherche")
    try:
        resultats = search.searchAndParse(query)
    except:
        print("pydcc.py : erreur searchAndParse")
    for ligne in resultats:
        print(ligne)
            
elif choix == 2 :

    # Pour tester en "vrai"
    channel="#BEAST-XDCC"
    nickname="Paul"
    server="irc.abjects.net"
    numPaquet=46
    nomRobot="Beast-US-026"
    secondChannel=""
    bot = bot.Grabator(
        channel,
        nickname,
        server,
        numPaquet,
        nomRobot,
        secondChannel
        )
    bot.start()
    
elif choix == 3 :
    bot = bot.Grabator()
    bot.start()
    
else:
        print(choix)

