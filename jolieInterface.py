#!/usr/bin/python
# -*- coding: utf8 -*-

from tkinter import *
import search
import bot
import threading
from config import *
import time

tableauCadreAvancement = []

class jolieInterface(Frame):

    def __init__(self, fenetre, oSynchro, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)
        self.fenetre = fenetre
                
        ##############################
        # pour la gestion des bots irc
        ##############################
        self.DLPool = []
        
        
        ############################################
        # un cadre rien que pour le titre de l'appli
        ############################################
        cadreTitre = Frame(self)
        cadreTitre.pack(fill=BOTH)
        self.titreAppli = Label(cadreTitre, text="*** PYDCC ***")
        self.titreAppli.pack()
        
        ##########################
        # le cadre de la recherche
        ##########################
        recherche = Frame(self)
        recherche.pack(fill=BOTH)
        # avec choix du moteur de recherche
        listeMoteurRecherche = Listbox(recherche,height=1)
        listeMoteurRecherche.insert(END, "ixirc.com")
        listeMoteurRecherche.pack(side="left", fill=BOTH)
        # un champ pour saisir les mots clés
        self.query = StringVar()
        champMotCles = Entry(recherche, textvariable=self.query, width=50)
        champMotCles.pack(side="left", fill=BOTH)
        # un bouton pour lancer la recherche
        boutonRecherche = Button(recherche, text="Rechercher", command=self.rechercher)
        boutonRecherche.pack(side="left", fill=BOTH)
        
        ######################################
        # un cadre pour afficher les resultats
        ######################################
        self.resultatsCadreMain = Frame(self)
        self.resultatsCadreMain.pack(fill=BOTH)
        self.construireCadreResultat()
        
        #####################################
        # un cadre pour effectuer des actions
        #####################################
        self.actions = Frame(self)
        self.actions.pack(fill=BOTH)
        # juste un bouton pour lancer le DL des cases cochées
        boutonTelecharger = Button(self.actions, text="Télécharger les cases cochées", command=self.telecharger)
        boutonTelecharger.pack(side="left", fill=BOTH)

        #####################################
        # un cadre pour voir avancement
        #####################################
        self.avancement = Frame(self)
        self.avancement.pack(fill=BOTH)
        self.threadAvancement = threading.Thread(None, refreshAvancement, None, (self.DLPool,oSynchro))
        self.threadAvancement.start()
        
        
    def getThreadAvancement(self):
        #stop = True
        #time.sleep(0.5)
        return self.threadAvancement
        
        
    def construireCadreResultat(self):
        self.resultatsCadre = Frame(self.resultatsCadreMain)
        self.resultatsCadre.pack(fill=BOTH)
        # des cadres pour mettre en forme les résultats (tableau ...)
        self.resultatsCadresTable = []
        for i in range(0,5):
            self.resultatsCadresTable.append(Frame(self.resultatsCadre,relief=RAISED, borderwidth=1))
            self.resultatsCadresTable[i].pack(side=LEFT, fill=BOTH)
        LabelaCocher = Label(self.resultatsCadresTable[0], text="A Cocher")
        LabelaCocher.pack(fill=X)
        LabelNom = Label(self.resultatsCadresTable[1], text="Nom")
        LabelNom.pack(fill=X)
        LabelTaille = Label(self.resultatsCadresTable[2], text="Taille")
        LabelTaille.pack(fill=X)
        LabelServeur = Label(self.resultatsCadresTable[3], text="Serveur")
        LabelServeur.pack(fill=X)
        LabelChannel = Label(self.resultatsCadresTable[4], text="Channel")
        LabelChannel.pack(fill=X)
        

    
    def rechercher(self):
        self.resultatsCadre.destroy()
        self.construireCadreResultat()
        
        self.aTelecharger = []
        i = 0
        
        self.resultats = search.searchAndParse(self.query.get())
        if self.resultats != None :
        
            #debug 
            #print(self.resultats)
        
            for result in self.resultats:
                frameTemporaire = Frame(self.resultatsCadresTable[1])
                frameTemporaire.pack(fill=X)
                self.aTelecharger.append(IntVar())
                caseTemporaire = Checkbutton(frameTemporaire,variable=self.aTelecharger[i])
                caseTemporaire.pack(side=LEFT, fill=X)
                LabelTemporaireTitre = Label(frameTemporaire, text=result[0])
                LabelTemporaireTitre.pack(side=LEFT, fill=X)
                LabelTemporaireTaille = Label(self.resultatsCadresTable[2], text=result[6])
                LabelTemporaireTaille.pack(fill=X)
                LabelTemporaireServeur = Label(self.resultatsCadresTable[3], text=result[1])
                LabelTemporaireServeur.pack(fill=X)
                LabelTemporaireChannel = Label(self.resultatsCadresTable[4], text=result[2])
                LabelTemporaireChannel.pack(fill=X)
                i += 1
            
        self.titreAppli["text"] = "action rechercher finie"
        
    def telecharger(self):
        for case in self.aTelecharger :
            if case.get() !=0 :
                resultatChoisi = self.aTelecharger.index(case)
                monResultat = self.resultats[resultatChoisi]
                #print(monResultat) #DEBUG
                nouveauDL = bot.Download(
                    monResultat[1],
                    monResultat[2],
                    monResultat[3],
                    monResultat[4],
                    ircDefaultNickname,
                    monResultat[0]
                    )
                # debug
                #nouveauDL = bot.Download()
                self.DLPool.append(nouveauDL)
                nouveauThread = threading.Thread(None, nouveauDL.startDL, None)
                nouveauThread.start()
                tableauCadreAvancement.append(Label(self.avancement, text="..."))
                tableauCadreAvancement[-1].pack(fill=X)
        self.aTelecharger = []

def refreshAvancement(DLPool, oSynchro):
    cadre = None
    while oSynchro.stop == False:
        i = 0
        for DL in DLPool:
            avancementString = "{} : {} - {:.1f}% : {:.1f} Mo / {:.1f} Mo".format(
                    DL.nomFichier, DL.status, DL.avancement,
                    DL.dejaTelechargeEnMo, DL.tailleEnOctets/1048576) #1024*1024
            tableauCadreAvancement[i]['text'] = avancementString
            i += 1
        time.sleep(0.5)
    print("ok, threadAvancement va se terminer")
    
class synchro:
    def __init__(self):
        self.stop = False
        