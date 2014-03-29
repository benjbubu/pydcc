#!/usr/bin/python
#Python2.X needed + IrcLib/Bot
import irclib
import ircbot

class Grabator(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.server.com",6667)], "nickname_to_change", "user_to_change")
    
    def on_welcome(self, serv, ev):
	serv.join("#channel")

if __name__ == "__main__":
    Grabator().start()
