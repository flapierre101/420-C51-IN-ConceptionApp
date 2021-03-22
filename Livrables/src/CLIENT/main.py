## -*- Encoding: UTF-8 -*-

from vue import *
from modele import *
from connexion import *

import urllib.request
import urllib.parse
import sys


import json

from subprocess import Popen
##################
class Controleur:
    def __init__(self):
        #self.urlserveur= "http://jmdeschamps.pythonanywhere.com"
        self.modele=Modele(self)
        self.connexion = Connexion()       
        self.urlserveur= self.connexion.urlserveur 
        self.vue=Vue(self)
        self.vue.afficherlogin("aaa@xyz.com","AAAaaa111")
        self.vue.root.mainloop()

    def telechargermodule(self,fichier):
        leurl=self.urlserveur+"/telechargermodule"
        params = {"fichier":fichier}
        reptext=self.appelserveur(leurl,params)
        rep=json.loads(reptext)
        fichier1=open("./SaaS_modules/"+fichier,"w")
        fichier1.write(rep)
        fichier1.close()
        usager=json.dumps([self.modele.nom,self.modele.compagnie])
        Popen([sys.executable, "./SaaS_modules/"+fichier,self.urlserveur,usager],shell=1).pid

    def identifierusager(self,nom,mdp):
        reponse = self.connexion.identifierusager(nom, mdp)
        if "inconnu" in reponse:
            self.vue.avertirusager("Erreur","Mot de passe ou identifiant non reconnnu \n\nReesayer?")
        else:
            self.modele.inscrireusager(reponse)
            self.vue.creercadreprincipal(self.modele)
            self.vue.changercadre("principal")

    def trouvermodules(self):
        return self.connexion.trouvermodules()

    def getEvent(self):
        return self.connexion.getEvent()

    def trouvermembres(self):
        return self.connexion.trouvermembres()

    # fonction d'appel normalisee, utiliser par les methodes du controleur qui communiquent avec le serveur
    def appelserveur(self, url,params):
        return self.connexion.appelserveur(url,params)

if __name__ == '__main__':
    c=Controleur()
    print("FIN DE PROGRAMME")