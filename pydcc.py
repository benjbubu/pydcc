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

monIHM = jolieInterface.jolieInterface(fenetre)

monIHM.mainloop()
