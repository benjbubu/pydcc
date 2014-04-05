#!/usr/bin/python
# -*- coding: utf8 -*-

## POUR DCCRECEIVE ?
from __future__ import print_function

import os
import struct
#import sys
#import argparse
#import irc.client
#import irc.logging

import irc.bot
import irc.strings
#from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
#import config as CONFIG


class Grabator(irc.bot.SingleServerIRCBot):
    def __init__(self, channel="#barakuun", nickname="Pydcc", server="irc.kottnet.net", port=6667):
        print(channel, nickname, server, port) #DEBUG
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.received_bytes = 0
    
    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)
        self.connection.buffer.errors = 'replace'
        # DEBUG : se connecter à un autre channel en parallèle :)
        #c.join("#barakuun2")

    def on_privmsg(self, c, e):
        pass
        self.do_command(e, e.arguments[0])
        
    def on_pubmsg(self, c, e):
        pass

    def on_dccmsg(self, connection, event):
        data = event.arguments[0]
        self.file.write(data)
        self.received_bytes = self.received_bytes + len(data)
        self.dcc.send_bytes(struct.pack("!I", self.received_bytes))

    def on_dccchat(self, c, e):
        pass

    def do_command(self, e, cmd):
        pass
        nick = e.source.nick
        self.monMaitre = nick
        c = self.connection
        cmdListe = cmd.split()
        
        if cmdListe[0] == "disconnect":
            self.disconnect()
        elif cmdListe[0] == "die":
            self.die()
        elif cmdListe[0] == "transferator":
            c.notice(nick, "je vais démarrer le transfert avec transferator "+cmdListe[1])
            c.notice("Transferator", "xdcc send "+cmdListe[1])
        else:
            c.notice(nick, "Not understood: " + cmd)
            c.notice(nick, "pydcc usage :")
            c.notice(nick, "  /msg pydcc disconnect")
            c.notice(nick, "  /msg pydcc die")
            c.notice(nick, "  /msg pydcc transferator #XX")
        
    def on_ctcp(self, connection, event):
        args = event.arguments[1].split()
        if args[0] != "SEND":
            return
        self.filename = os.path.basename(args[1])
        if os.path.exists(self.filename):
            print("A file named", self.filename,)
            print("already exists. Refusing to save it.")
            self.connection.quit()
        self.file = open(self.filename, "wb")
        peeraddress = irc.client.ip_numstr_to_quad(args[2])
        peerport = int(args[3])
        self.dcc = self.dcc_connect(peeraddress, peerport, "raw")
          
    def on_dcc_disconnect(self, connection, event):
        self.file.close()
        print("Received file %s (%d bytes)." % (self.filename,
                                                self.received_bytes))
        #self.connection.quit()


if __name__ == "__main__":
    print("bot.py - fonction test")
    bot = Grabator()
    bot.start()
