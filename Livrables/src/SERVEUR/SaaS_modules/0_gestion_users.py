# à copier dans chaque nouveau module pour avoir la classe connexion
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../connexion.py
from connexion import *


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()

    def createModuleFrame(self):
        pass

    def createButtonFrame(self):
        pass



class Modele():
    def __init__(self, parent):
        self.parent = parent


class Controleur():
    def __init__(self):
        self.nomUser = sys.argv[1]
        self.modele = Modele(self)
        self.connexion = Connexion()
        self.urlserveur = self.connexion.urlserveur
        self.vue = Vue(self)
        self.vue.root.mainloop()

if __name__ == '__main__':
    c = Controleur()
