#!/usr/bin/python
#
# PYDCC main program - User Interface
#


import urllib2
import config as CONFIG
import seach
        
print "Pydcc"
print " 1 : Rechercher"
print " 2 : Voir le DL en cours"
choix = input("Quel est votre choix?")

if choix == 1:
        query = raw_input("Indiquez votre recherche \n")
        url = "http://ixirc.com/?q=%s" % query.replace(" ","+")
        recherche = urllib2.urlopen(url)
        html = recherche.read()
        print(url)
        #print(html)
else:
        print(choix)

