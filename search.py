#!/usr/lib/python
#
# FUNCTIONS TO SEARCH AND PARSE RESULTS
#

import urllib2
import config as CONFIG
        
def search(requete, url=CONFIG.url):
        url = "http://ixirc.com/?q=%s" % requete.replace(" ","+")
        recherche = urllib2.urlopen(url)
        html = recherche.read()
        return html

