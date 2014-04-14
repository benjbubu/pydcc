#!/usr/bin/python
# -*- coding: utf8 -*-

## POUR DCCRECEIVE ?
#from __future__ import print_function
import os
import struct
import irc.bot
import irc.strings
#from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from config import *
import re
import random


def download(connection, nomRobot, numPaquet):
    print("commande XDCC SEND #" + str(numPaquet) )
    connection.notice(nomRobot, "xdcc send #" + str(numPaquet) )

def checkTerminated(bot, DL):
    if DL.terminated == True :
        bot.die()

################################################################################
# CLASS Grabator
################################################################################    
class Grabator(irc.bot.SingleServerIRCBot):
    """
        class Grabator
        
        définit un bot qui se connecte à un serveur irc et est capable de 
        télécharger des paquets en xdcc.
        Il peut scanner le topic du channel principal ainsi que les messages
        privés afin de se connecter aux salons et channels de chat.
    
    """
    def __init__(
            self, 
            objetDL,
            channel = ircDefaultChannel, 
            nickname = ircDefaultNickname, 
            server = ircDefaultServer, 
            numPaquet = ircDefaultNumPaquet, 
            nomRobot = ircDefaultNomRobot, 
            secondChannel = ircDefaultSecondChannel,
            port = ircDefaultPort
            ):
        print("channel =", channel, "; nickname =", nickname, "; server = ", server, port) #DEBUG
        try:
            irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        except:
            print("bot.py : pb création bot/connexion server")
        self.objetDL = objetDL
        self.channel = channel
        self.numPaquet = numPaquet
        self.nomRobot = nomRobot
        self.secondChannel = secondChannel
        self.received_bytes = 0
        self.ctcp_version = ircDefaultVersion
        self.repriseDL = False
        # Pour gérer les encodages :
        self.connection.buffer_class.encoding = 'utf-8'# self.connection.buffer_class. = irc.buffer.LineBuffer
        
        self.connection.execute_every(0.5, checkTerminated, (self, self.objetDL ) )
        
    #def __del__(self):
    
    def on_nicknameinuse(self, c, event):
        c.nick(c.get_nickname() + "_")
        
    def on_welcome(self, connection, event):
        connection.join(self.channel)
        
        # pour gérer les problème d'encodage
        self.connection.buffer.errors = 'replace'
        
        if (self.secondChannel != ""):
            print("connexion au secondChannel :", self.secondChannel)
            connection.join(self.secondChannel)
        
        # tempo et commande pour téléchargement
        connection.execute_delayed(random.uniform(2,8), download, (connection, self.nomRobot, self.numPaquet) )
    
    def on_privmsg(self, connection, event):
        #DEBUG
        print("priv --", event.arguments)
        msgPriv = self.filtrerCouleur(event.arguments[0])
        secondChannel = self.extraireChannel(msgPriv)
        if ( secondChannel is not None ) :
            if (secondChannel != self.channel):
                self.secondChannel = secondChannel
                print( "connexion au second channel : ", self.secondChannel)
                connection.join(self.secondChannel)
        else:
            print( "Pas de channel dans le message privé")
        
    def on_pubmsg(self, cconnection, event):
        pass
        #DEBUG
        #print("pub ---", event.arguments)

    def on_dccmsg(self, connection, event):
        #DEBUG
        #print("dccmsg --", event.arguments)
        
        data = event.arguments[0]
        self.file.write(data)
        self.received_bytes = self.received_bytes + len(data)
        
        # synchro des infos avec le programme principal
        self.objetDL.dejaTelechargeEnMo = self.received_bytes/1048576 # 1024*1024
        self.objetDL.avancement = self.received_bytes/self.objetDL.tailleEnOctets*100
        
        self.dcc.send_bytes(struct.pack("!I", self.received_bytes))

    def on_dccchat(self, connection, event):
        pass

    def do_command(self, event, cmd):
        pass

    def on_ctcp(self, connection, event):
        #DEBUG
        print("on_ctcp --", event.arguments)
        
        nick = event.source.nick
        # Repondre à :
        
        # VERSION
        if event.arguments[0] == "VERSION":
            connection.ctcp_reply(nick, "VERSION " + self.ctcp_version)
            
        # PING
        elif event.arguments[0] == "PING":
            if len(event.arguments) > 1:
                connection.ctcp_reply(nick, "PING " + event.arguments[1])
                
        # SEND => TELECHARGER
        elif len(event.arguments) >= 2:       
            args = event.arguments[1].split()
            if args[0] == "SEND":
                self.filename = downloadPath + os.path.basename(args[1])
                if os.path.exists(self.filename):
                    print("A file named", self.filename,)
                    print("already exists. Attempting to resume it.")
                    #self.connection.quit()
                    #self.die()
                    self.objetDL.tailleEnOctets = int(args[4])
                    self.peeraddress = irc.client.ip_numstr_to_quad(args[2])
                    position = os.path.getsize(self.filename)
                    #print("commande XDCC RESUME  position=" + str(position) )
                    cmd = "DCC RESUME #"+ str(self.numPaquet) +" "+ str(args[3]) +" "+ str(position)
                    print(cmd)
                    connection.ctcp_reply(self.nomRobot, cmd  )
                    # self.file = open(self.filename, "ab")
                    # peeraddress = irc.client.ip_numstr_to_quad(args[2])
                    # peerport = int(args[3])
                    # self.dcc = self.dcc_connect(peeraddress, peerport, "raw")
                else:
                    print("Pas de fichier existant. Debut du DL")                    
                    # récupération de la taille en Octets du fichier
                    self.objetDL.tailleEnOctets = int(args[4])
                    # 
                    self.file = open(self.filename, "wb")
                    peeraddress = irc.client.ip_numstr_to_quad(args[2])
                    peerport = int(args[3])
                    self.dcc = self.dcc_connect(peeraddress, peerport, "raw")
            elif args[0] == "ACCEPT" :
                print("on_ctcp RESUME")
                self.file = open(self.filename, "ab")
                peerport = int(args[2])
                self.dcc = self.dcc_connect(self.peeraddress, peerport, "raw")
            else:
                print("bot.py : error : dcc command incomprise")
                self.die()
          
    def on_dcc_disconnect(self, connection, event):
        self.file.close()
        print("Received file %s (%d bytes)." % (self.filename,
                                                self.received_bytes))
        print("Maintenant, je vais me coucher, ciao")
        self.objetDL.status = "fini"
        self.objetDL.avancement = 100
        self.die()

    def on_currenttopic(self, connection, event):
        topic = self.filtrerCouleur(event.arguments[1])
        secondChannel = self.extraireChannel(topic)
        if ( secondChannel is not None ) :
            if (secondChannel != self.channel):
                self.secondChannel = secondChannel
                print( "connexion au second channel : ", self.secondChannel)
                connection.join(self.secondChannel)
        else:
            print( "Pas de channel dans le topic")
    
    def filtrerCouleur(self, string):
        return re.sub(
            '(\\03..\,.)|(\\x03[0-9][0-9])|(\\x03[0-9])|(\\x03)|(\\x1f)|(\\x02)',
            '',
            string)
    
    def extraireChannel(self, string) :
        channel = re.findall('\#\S*',string)
        if (channel == [] ):
            return None
        else :
            return channel[0] 
            
            

################################################################################
# CLASS botFactory
################################################################################    
class Download :
    def __init__(
            self,
            server = ircDefaultServer,
            channel = ircDefaultChannel,
            nomRobot = ircDefaultNomRobot,
            numPaquet = ircDefaultNumPaquet,
            nickname  =ircDefaultNickname,
            nomFichier = "Pas de nom défini",
            secondChannel = ircDefaultSecondChannel,
            port = ircDefaultPort
            ):
        self.server = "irc." + server + ".net"
        self.channel = channel
        self.nomRobot = nomRobot
        self.numPaquet = numPaquet
        self.nickname = nickname
        self.secondChannel = secondChannel
        self.nomFichier = nomFichier
        self.port = port
        
        # et pour le partage d'infos :
        self.terminated = False       
        self.dejaTelechargeEnMo = 0
        self.tailleEnOctets = 1048576
        self.status = "pas commencé"
        self.avancement = 0
        
    def startDL(self):
        self.status = "en cours"
        self.pydccBot = Grabator(
            self,
            self.channel,
            self.nickname, 
            self.server,
            self.numPaquet,
            self.nomRobot,
            self.secondChannel,
            self.port
            )
        self.pydccBot.start()

        
        
            
# TEST DE LA CLASSE GRABATOR, UN XDCC_BOT
if __name__ == "__main__":
    print("bot.py - fonction test")
    bot = Grabator()
    bot.start()
