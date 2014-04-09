#!/usr/lib/python
# -*- coding: utf8 -*-
#
# FUNCTIONS TO SEARCH AND PARSE RESULTS
#

import urllib.request
from config import *
from bs4 import BeautifulSoup
        
def searchAndParse(requete, url = defaultUrl):
    """
        searchAndParse(requete, url=CONFIG.url)
        
        Effectue une requête sur un site de recherche xdcc,
        récupère le code source de la page 
        et parse le code source pour obtenir une liste des downloads
        
        Contenu d'une ligne de Resultats dans l'ordre :
            1-titre
            2-serveur
            3-channel
            4-user
            5-numero du paquet
            6- ?
            7-taille
            8- ?
            9- ?
    """
    
    try:
        # REQUETE WEB ET RECUPERATION CODE SOURCE HTML
        url = (url + "%s") % requete.replace(" ","+")
        html = urllib.request.urlopen(url).read()
    except:
        print("searchAndPaste : erreur récupération page html")
    
    try:
        # PARSE LE CODE HTML pour le site http://ixirc.com
        soup = BeautifulSoup(html)
        resultats = []
        nbreResultat = 0
        # Les résultats sont dans la seule balise <table> de la page
        table = soup.find('table')
        tr_s = table.find_all('tr')
        
        for tr in tr_s:
            # On sélectionne une ligne du tableau
            td_s = tr.find_all('td')
            resultats.append([])
            
            for data in td_s:
                # On sélectionne une cellule de la ligne
                try:
                    info = data.get_text()
                    if info:
                        resultats[nbreResultat].append(info)
                except:
                    print("searchAndParse - boucle td_s : erreur")
                    
            nbreResultat += 1
    except:
            print("searchAndPaste : erreur parser BeautifulSoup")
 
    return resultats
        
