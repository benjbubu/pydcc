#!/usr/bin/python
#Python2.X needed + IrcLib/Bot
import irclib
import ircbot
import config as CONFIG

class Grabator(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [(CONFIG.ircServerName,CONFIG.ircPort)], CONFIG.ircNickname, CONFIG.ircUserName)
    
    def on_welcome(self, serv, ev):
	serv.join(CONFIG.ircChannel)

if __name__ == "__main__":
    Grabator().start()
