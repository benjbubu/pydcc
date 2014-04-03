#!/usr/lib/python
# -*- coding: utf8 -*-
#
# FUNCTIONS TO SEARCH AND PARSE RESULTS
#

import urllib.request
import config as CONFIG
from bs4 import BeautifulSoup
        
def searchAndParse(requete, url=CONFIG.url):
        try:
                url = "http://ixirc.com/?q=%s" % requete.replace(" ","+")
                html = urllib.request.urlopen(url).read()
        except:
                print("searchAndPaste : erreur récupération page html")
        
        try:
                soup = BeautifulSoup(html)
        
                # Version 1 : pas testé
                #tableResultat = soup.find(id="results-table")
                #table = BeautifulSoup(tableResultat)
                #nbreResultat = 0
                #resultats = []
                #for ligne in tableResultat.find_all(tr) :
                #        resultats[nbreResultats] = []
                #        for a in ligne.find_all(a):
                #                resultats[nbreResultats].append(a.string)
                #                # Resultats dans l'ordre 
                #                # 1-titre
                #                # 2-serveur
                #                # 3-channel
                #                # 4-user
                #                # 5- ?
                #                # 6- ?
                #                # 7-taille
                #                # 8- ?
                #                # 9- ?
                #        nbreResultat += 1
                
                # Version 2
                #table = soup.findAll('a', {'class':'result-dl'})
                #print(len(table))
                #resultats = []
                #for ligne in table :
                #    resultats.append(ligne.get('href'))
                #    print(ligne.string)
                
                #Version 3
                resultats = []
                nbreResultat = 0
                table = soup.find('table')
                tr_s = table.find_all('tr')
                for tr in tr_s:
                    #print(tr,"\n\n") ## DEBUG
                    td_s = tr.find_all('td')
                    #print(td_s,"\n\n\n---------------") #DEBUG
                    resultats.append([])
                    for data in td_s:
                        try:
                            #print(data,"\n\n") #DEBUG
                            #info = data.string
                            info = data.get_text()
                            #print(info,"\n\n\n------") #DEBUG
                            if info:
                                resultats[nbreResultat].append(info)
                        except:
                            print("searchAndParse - boucle td_s : erreur")
                        finally:
                            None
                    nbreResultat += 1
                
        except:
                print("searchAndPaste : erreur parser BeautifulSoup")
     
        return resultats
        
