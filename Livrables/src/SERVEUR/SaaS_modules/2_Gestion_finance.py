## -*- Encoding: UTF-8 -*-
import urllib.request
import urllib.parse

from tkinter import *
from tkinter.simpledialog import *
from tkinter import ttk

import json
class Vue():
    def __init__(self,parent):
        self.parent=parent
        self.root=Tk()
        self.root.title("Production CDJ - Finance")
        self.cadreapp=Frame(self.root)
        self.canevas=Canvas(self.cadreapp,width=800,height=600)
        self.canevas.create_text(400,300,anchor=CENTER,text='Module "Finance" est en construction \nPrévu pour la version 2.0 en automne 2021')
        self.canevas.pack()
        self.cadreapp.pack()

class Controleur():
    def __init__(self):
        self.vue=Vue(self)
        self.vue.root.mainloop()

if __name__ == '__main__':
    c=Controleur()