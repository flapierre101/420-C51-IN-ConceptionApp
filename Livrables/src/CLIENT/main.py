## -*- Encoding: UTF-8 -*-

from vue import *
from modele import *
from connexion import *


##################
class Controleur:
    def __init__(self):
        self.modele=Modele(self)
        self.connexion = Connexion()
        self.urlserveur= self.connexion.urlserveur
        self.vue=Vue(self)
        self.vue.afficherlogin("aaa@xyz.com","AAAaaa111")
        self.vue.root.mainloop()

    def getcompagnie(self):
        return self.modele.compagnie

    def telechargermodule(self,fichier):
        self.connexion.telechargermodule(fichier, self.modele.nom, self.modele.droit, self.modele.courriel, self.modele.compagnie)

    def identifierusager(self,courriel,mdp):
        reponse = self.connexion.identifierusager(courriel, mdp)
        if "inconnu" in reponse:
            self.vue.avertirusager("Erreur","Mot de passe ou identifiant non reconnnu \n\nReesayer?")
        else:
            self.modele.inscrireusager(reponse, courriel)
            self.vue.creercadreprincipal(self.modele)
            self.vue.changercadre("principal")

    def trouvermodules(self):
        return self.connexion.trouvermodules()

    def getEvent(self):
        return self.connexion.getEvent()

    def trouvermembres(self):
        return self.connexion.trouvermembres()

    def changerForfait(self, forfait):
        self.modele.compagnie["forfait"] = forfait
        return self.connexion.changerForfait(forfait, self.modele.compagnie["id"])

    # fonction d'appel normalisee, utiliser par les methodes du controleur qui communiquent avec le serveur
    def appelserveur(self, url,params):
        return self.connexion.appelserveur(url,params)

if __name__ == '__main__':
    c=Controleur()
    print("FIN DE PROGRAMME")
