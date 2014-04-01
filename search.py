#!/usr/lib/python
#
# FUNCTIONS TO SEARCH AND PARSE RESULTS
#

import urllib.request
import config as CONFIG
<<<<<<< HEAD
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
                table = soup.findAll('a', {'class':'result-dl'})
                resultats = []
                for ligne in table :
                    resultats.append(ligne.get('href'))
                    print(ligne.get('href'))
        except:
                print("searchAndPaste : erreur parser")
        
        
=======
from BeautifulSoup import BeautifulSoup
        
def search(requete, url=CONFIG.url):
        url = "http://ixirc.com/?q=%s" % requete.replace(" ","+")
        recherche = urllib2.urlopen(url).read()
        #html = recherche.read()
        return url

def parse(html):
        soup = BeautifulSoup(html)
        tableResultat = soup.find(id="results-table")
        nbreResultat = 0
        resultats = []
        for ligne in tableResultat.find_all(tr) :
                resultats[nbreResultats] = []
                for a in ligne.find_all(a):
                        resultats[nbreResultats].append(a.string)
                        # Resultats dans l'ordre 
                        # 1-titre
                        # 2-serveur
                        # 3-channel
                        # 4-user
                        # 5- ?
                        # 6- ?
                        # 7-taille
                        # 8- ?
                        # 9- ?
                nbreResultat += 1
>>>>>>> ab667c788e41ac60a547801ff4b773899921edd4
        return resultats
        
