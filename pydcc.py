#!/usr/bin/python
# -*- coding: utf8 -*-
#
# PYDCC main program - User Interface
#

from config import *
import search
import bot
import threading

# import os
# import time


    
## MAIN PROGRAMM

choix = 666
DLPool = []


try:
    while choix != 0:

        # MENU
        print("Pydcc")
        print(" 1 : Rechercher")
        print(" 2 : voir les dl en cours")
        print(" 3 : TEST => lancer le bot pour test sur abjects")
        print(" 4 : TEST => lancer le bot sur #barakuun")
        print(" 0 : quitter")

        try:
            choix = input("Quel est votre choix?\n")
            choix = int(choix)
        except:
            print("pydcc.py : erreur saisie/conversion choix")

        # RECHERCHE ET LANCEMENT DL
        if choix == 1 :
            try:
                query = input("Indiquez votre recherche \n")
            except:
                print("pydcc.py : erreur input recherche")
            try:
                resultats = search.searchAndParse(query)
            except:
                print("pydcc.py : erreur searchAndParse")
            
            # Affiche les résultats de la recherche :
            i = 1
            for ligne in resultats:
                print(i, ":", ligne)
                i += 1
                
            # Choix du DL
            print("Votre choix ? (0 = revenir en arrière)")
            resultatChoisi = input("Quel DL choisissez vous ?\n")
            resultatChoisi = int(resultatChoisi)
            if resultatChoisi == 0:
                pass
            else:
                # Contenu d'une ligne de Resultats dans l'ordre :
                # 0-titre
                # 1-serveur
                # 2-channel
                # 3-user
                # 4-numero du paquet
                # 5- ?
                # 6-taille
                # 7- ?
                # 8- ?
                resultatChoisi -= 1 # en python, les listes commencent à 0 !!
                monResultat = resultats[resultatChoisi]
                print(monResultat) #DEBUG
                nouveauDL = bot.Download(
                    monResultat[1],
                    monResultat[2],
                    monResultat[3],
                    monResultat[4],
                    ircDefaultNickname,
                    monResultat[0]
                    )
                DLPool.append(nouveauDL)
                nouveauThread = threading.Thread(None, nouveauDL.startDL, None)
                nouveauThread.start()
        
        # VISU DES DL EN COURS
        elif choix == 2 :
            for DL in DLPool:
                print("{} : {} - {:.1f}% : {:.1f} Mo / {:.1f} Mo".format(
                    DL.nomFichier, DL.status, DL.avancement,
                    DL.dejaTelechargeEnMo, DL.tailleEnOctets/1048576) #1024*1024
                    ) 
                
            # ANCIENNES SOLUTIONS :    
            # while botPool[0].isAlive() :
                # print("x =",search.x/1000000, "Mo")

                # if os.path.isfile("soser.iso"):
                    # print("os.path.getsize :", os.path.getsize("soser.iso")/1000000 )
                    
                # time.sleep(1)

        
        # TEST EN "VRAI"
        elif choix == 3 :

            # Pour tester en "vrai"
            nouveauDL = bot.Download(
                "abjects",
                "#BEAST-XDCC",
                "Beast-US-026",
                46,
                "Georges",
                )
            DLPool.append(nouveauDL)
            nouveauThread = threading.Thread(None, nouveauDL.startDL, None)
            nouveauThread.start()
            
        # TEST SUR TRANSFERATOR
        elif choix == 4 :
            nouveauDL = bot.Download()
            DLPool.append(nouveauDL)
            nouveauThread = threading.Thread(None, nouveauDL.startDL, None)
            nouveauThread.start()
            
            
        # QUITTER
        elif choix == 0 :
            pass
            
        else:
                print(choix, " : choix invalide")
                
finally:
    print("Vous êtes en train de commettre un génocide de bots irc !")
    print("Quitte pydcc et arrête tous les téléchargements en cours")
    print("See you soon")
    
    for DL in DLPool:
        DL.terminated = True
