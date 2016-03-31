#!/usr/bin/python
# -*- coding: utf8 -*-
#
# PYDCC main program - User Interface
#

from config import *
import jolieInterface


from tkinter import *

# On crée une fenêtre, racine de notre interface
fenetre = Tk()

oSynchro = jolieInterface.synchro()

monIHM = jolieInterface.jolieInterface(fenetre, oSynchro)

monIHM.mainloop()

oSynchro.stop = True
