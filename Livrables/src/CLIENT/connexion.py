import urllib.request
import urllib.parse
import sys
import os

import json

from subprocess import Popen

class Connexion:
    def __init__(self):
        self.urlserveur="http://127.0.0.1:5000"

    def trouvermembres(self):
        url = self.urlserveur+"/trouvermembres"
        params = {}
        reptext=self.appelserveur(url,params)

        mondict=json.loads(reptext)
        return mondict

    def getEvent(self):
        url = self.urlserveur+"/getEvent"
        params = {}
        reptext=self.appelserveur(url,params)
        mondict=json.loads(reptext)
        return mondict

    def trouvermodules(self):
        url = self.urlserveur+"/trouvermodules"
        params = {}
        reptext=self.appelserveur(url,params)

        mondict=json.loads(reptext)
        return mondict

        # fonction d'appel normalisee, utiliser par les methodes du controleur qui communiquent avec le serveur
    def appelserveur(self,url,params):
        query_string = urllib.parse.urlencode( params )
        data = query_string.encode( "ascii" )
        url = url + "?" + query_string
        rep=urllib.request.urlopen(url , data)
        reptext=rep.read()
        return reptext

    def identifierusager(self,nom,mdp):
        url = self.urlserveur+"/identifierusager"
        params = {"nom":nom,
                "mdp":mdp}
        reptext=self.appelserveur(url,params)

        return json.loads(reptext)

    def telechargermodule(self,fichier, usager, compagnie):
        leurl=self.urlserveur+"/telechargermodule"
        params = {"fichier":fichier}
        reptext=self.appelserveur(leurl,params)
        rep=json.loads(reptext)
        os.makedirs("./SaaS_modules/", exist_ok=True) # creation du dossier SaaS_module s'il n'existe pas
        fichier1=open("./SaaS_modules/"+fichier,"w")
        fichier1.write(rep)
        fichier1.close()
        usager=json.dumps([usager, compagnie])
        Popen([sys.executable, "./SaaS_modules/"+fichier,self.urlserveur,usager],shell=1).pid

    def saveEvent(self, newEvent):
        url = self.urlserveur + "/newEvent"
        rep = self.appelserveur(url, newEvent)
        return "Nouvel évènement enregistré"

    def deleteEvent(self, eventID):
        url = self.urlserveur + "/deleteEvent"
        params = {"id":eventID}
        rep = self.appelserveur(url, params)
        rep = json.loads(rep)
        if rep == "Success":
            return "Évènement supprimé avec succès"
        else:
            return "Une erreur est survenue"

    def updateEvent(self, updateData):
        url = self.urlserveur + "/updateEvent"
        rep = self.appelserveur(url, updateData)

        return rep

    def getEvent(self):
        url = self.urlserveur+"/getEvent"
        params = {}
        reptext=self.appelserveur(url,params)
        mondict=json.loads(reptext)
        return mondict

    def changerForfait(self, forfait, compagnieID):
        url = self.urlserveur+"/updateForfait"
        params = {"forfait":forfait, "compagnieID": compagnieID}
        reptext=self.appelserveur(url,params)
        mondict=json.loads(reptext)
        print(mondict)
        return mondict