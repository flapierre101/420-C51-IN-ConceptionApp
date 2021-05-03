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

    def telechargermodule(self,fichier, usager, droit, courriel, compagnie):
        leurl=self.urlserveur+"/telechargermodule"
        params = {"fichier":fichier}
        reptext=self.appelserveur(leurl,params)
        rep=json.loads(reptext)
        os.makedirs("./SaaS_modules/", exist_ok=True) # creation du dossier SaaS_module s'il n'existe pas
        fichier1=open("./SaaS_modules/"+fichier,"w")
        fichier1.write(rep)
        fichier1.close()
        compagnie=json.dumps(compagnie)
        Popen([sys.executable, "./SaaS_modules/"+fichier,droit,usager, courriel, compagnie],shell=1).pid

    def saveEvent(self, newLivrable):
        url = self.urlserveur + "/newLivrable"
        rep = self.appelserveur(url, newLivrable)
        return "Nouvel évènement enregistré"

    def saveUser(self, newUser):
        url = self.urlserveur + "/newUser"
        rep = self.appelserveur(url, newUser)
        rep = json.loads(rep)

        if rep == "Success":
            return "Nouvel utilisateur créé avec succès"
        else:
            return "Une erreur est survenue"

    def deleteEvent(self, livrableID):
        url = self.urlserveur + "/deleteEvent"
        params = {"id":livrableID}
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

    def getRoles(self):
        url = self.urlserveur + "/getRoles"
        params = {}
        reptext = self.appelserveur(url,params)
        mondict = json.loads(reptext)
        return mondict

    def getPermissions(self):
        url = self.urlserveur + "/getPermissions"
        params = {}
        reptext = self.appelserveur(url,params)
        mondict = json.loads(reptext)
        return mondict

    def getCompanyID(self, compagnie):
        url = self.urlserveur+"/getCompanyID"
        params = {"compagnie":compagnie}
        rep = self.appelserveur(url,params)
        rep = json.loads(rep)
        return rep

    def changerForfait(self, forfait, compagnieID):
        url = self.urlserveur+"/updateForfait"
        params = {"forfait":forfait, "compagnieID": compagnieID}
        reptext=self.appelserveur(url,params)
        mondict=json.loads(reptext)
        return mondict


    def saveLivrable(self, newLivrable):
        url = self.urlserveur + "/newLivrable"
        rep = self.appelserveur(url, newLivrable)
        return "Nouveau livrable enregistré"

    def deleteLivrable(self, livrableID):
        url = self.urlserveur + "/deleteLivrable"
        params = {"id":livrableID}
        rep = self.appelserveur(url, params)
        rep = json.loads(rep)
        if rep == "Success":
            return "Livrable supprimé avec succès"
        else:
            return "Une erreur est survenue"

    def completeLivrable(self, id, valeur):
        url = self.urlserveur + "/completeLivrable"
        params = { "valeur" : valeur,
                    "id" : id}
        rep = self.appelserveur(url, params)
        return rep

    def getLivrables(self, courriel, complete):
        url = self.urlserveur+"/getLivrables"
        params = {"courriel" : courriel, "complete": complete}
        reptext=self.appelserveur(url,params)
        mondict=json.loads(reptext)
        return mondict

    def getEcheanciers(self, idEvent):
        url = self.urlserveur+"/getEcheanciers"
        params = {"event" : idEvent}
        reptext=self.appelserveur(url,params)
        mondict=json.loads(reptext)
        return mondict

    def populate(self, table, id):
        url = self.urlserveur+"/populate"
        params = { "table" : table,
                    "id" : id}
        reptext=self.appelserveur(url,params)
        mondict=json.loads(reptext)
        #print(mondict)
        return mondict

    def save_client(self, newclient):
        url = self.urlserveur + "/save_client"
        self.appelserveur(url, newclient)
        return "Nouveau Client enregistré"

    def delete_client(self, clientID):
        url = self.urlserveur + "/deleteClient"
        params = {"id":clientID}
        rep = self.appelserveur(url, params)
        rep = json.loads(rep)
        print(rep)
        if rep == "Success":
            return "Client supprimé avec succès"
        else:
            return "Une erreur est survenue"

    def updateClient(self, updateData):
        url = self.urlserveur + "/updateClient"
        rep = self.appelserveur(url, updateData)
        

        return rep

    def getClients(self):
        url = self.urlserveur+"/getClients"
        params = {}
        reptext=self.appelserveur(url,params)
        mondict=json.loads(reptext)
        return mondict

    def updateLivrable(self, params):
        url = self.urlserveur + "/updateLivrable"
        rep = self.appelserveur(url, params)
        print(rep)
