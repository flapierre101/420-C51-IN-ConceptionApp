## -*- Encoding: UTF-8 -*-
import urllib.request
import urllib.parse

from tkinter import *
from tkinter.simpledialog import *
from tkinter import ttk
from tkinter.ttk import Style

import json
class Vue():
    def __init__(self,parent):
        self.parent=parent
        self.root=Tk()
        self.root.tk.call('lappend', 'auto_path', './Styles/awthemes-10.3.0')
        self.root.tk.call('package', 'require', 'awdark')
        self.root.tk.call('package', 'require', 'awlight')
        self.style = Style(self.root)
        # self.style.theme_use("awlight")
        # self.root.configure(bg='#e8e8e7')
        self.style.theme_use("awdark")
        self.root.configure(bg='#33393b')
        self.root.title("Production CDJ - Inventaire")
        self.cadreapp=Frame(self.root)
        self.canevas=Canvas(self.cadreapp,width=800,height=600)
        self.canevas.create_text(400,300,anchor=CENTER,text='Module "Inventaire" est en construction \nPrévu pour la version 2.0 en automne 2021')
        self.canevas.pack()
        self.cadreapp.pack()

class Controleur():
    def __init__(self):
        self.vue=Vue(self)
        self.vue.root.mainloop()

if __name__ == '__main__':
    c=Controleur()