#!/usr/lib/python
#
# FUNCTIONS TO SEARCH AND PARSE RESULTS
#

import urllib2
import config as CONFIG
        
def search(requete, url=CONFIG.url):
        url = "http://ixirc.com/?q=%s" % requete.replace(" ","+")
        recherche = urllib2.urlopen(url).read()
        #html = recherche.read()
        return html

def parse(html):
        soup = BeautifulSoup(html)
        tableResultat = soup.find(id="results-table")
        nbreResultat = 0
        resultats = []
        for ligne in tableResultat.find_all(tr) :
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
        return resultats
        
