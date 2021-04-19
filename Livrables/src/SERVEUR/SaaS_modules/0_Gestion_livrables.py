
from tkinter import *
from tkinter.ttk import *
from tkcalendar import *
import urllib.request
import urllib.parse
from flask import json
import datetime
import sys
import re


# à copier dans chaque nouveau module pour avoir la classe connexion
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../connexion.py
from connexion import *

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.livrableInfo = {}
        self.livrable = {}
        self.livrableParam = {}
        self.messageLabel = None
        self.welcomeLabel = Label(
            self.root, text="Bienvenue " + self.parent.getUsername(), font=("Arial", 14)).pack()
        self.title = Label(
            self.root, text="*** Gestion des livrables ***", font=("Arial", 16)).pack()
        self.createModuleFrame()

    def createModuleFrame(self):
        self.gestionFrame = Frame(self.root)
        self.listeLivrables = self.parent.getLivrables()
        self.root.geometry("325x325")
        self.listFrame = Frame(self.gestionFrame)
        self.buttonFrame = Frame(self.gestionFrame)
        self.livrableList = Listbox(self.listFrame, width=30)

        row = 1        
        for i in self.listeLivrables:
            self.livrableList.insert(row, i[1])
            row += 1

        listLabel = Label(self.listFrame, text="Liste des livrables")
        listLabel.pack()
        self.livrableList.pack()

        self.listFrame.pack(side=LEFT)

        self.createButtonFrame()
        self.buttonFrame.pack()
        self.gestionFrame.pack()

    def createButtonFrame(self):
        self.createLibrable = Button(
            self.buttonFrame, text="Créer un livrable", command=self.createLivrable)
        self.livrableDetailButton = Button(
            self.buttonFrame, text="Détail du livrable", command=self.livrableDetails)

        self.createLibrable.pack(fill=Y)
        self.livrableDetailButton.pack(fill=Y)

    def createLivrable(self):
        self.gestionFrame.destroy()
        self.createLivrableFrame()

    def createLivrableFrame(self):
        self.root.geometry("325x325")
        self.livrableFrame = Frame(self.root)
        self.infoFrame = Frame(self.livrableFrame)
        self.buttonFrame = Frame(self.livrableFrame)
        self.confirmationFrame = Frame(self.livrableFrame)

        self.createInfoFrame()
        self.createLibrableFrame()

        title = Label(self.livrableFrame,
                      text="* Créer un livrable *", font=("Arial", 14))
        title.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack()
        self.livrableFrame.pack()
        self.confirmationFrame.pack(pady=10)

    def createDetailsFrame(self):
        self.root.geometry("325x325")
        self.livrableFrame = Frame(self.root)
        self.infoFrame = Frame(self.livrableFrame)
        self.buttonFrame = Frame(self.livrableFrame)
        self.confirmationFrame = Frame(self.livrableFrame)

        self.createInfoDetailsFrame()

        title = Label(self.livrableFrame,
                      text="* Modifier un évènement *", font=("Arial", 14))
        title.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack()
        self.livrableFrame.pack()
        self.confirmationFrame.pack(pady=10)

    def createInfoDetailsFrame(self):
        fields = ["Nom", "Budget", "Description"]
        row = 0

        for i in fields:

            entryLabel = Label(self.infoFrame, text=i)

            if "Nom" in i:
                entry = Entry(self.infoFrame)
                entry.insert(0, self.livrable["desc"])

            elif "Budget" in i:
                entry = Entry(self.infoFrame)
                entry.insert(0, self.livrable["desc"])
            else:
                entry = Entry(self.infoFrame)
                entry.insert(0, self.livrable["desc"])

            entryLabel.grid(row=row, column=0, sticky=E + W)
            entry.grid(row=row, column=1, sticky=E + W)
            row += 1
            self.livrableInfo[i] = entry

    def createDetailsButtonFrame(self):
        self.updatelivrableButton = Button(
            self.buttonFrame, text="Modifier", command=self.updateLivrable)
        self.backButton = Button(
            self.buttonFrame, text="Retour au menu", command=self.backToMenu)
        self.deleteLivrableButton = Button(
            self.buttonFrame, text="Supprimer le livrable", command=self.deleteLivrable)
        self.updatelivrableButton.pack(side=LEFT)
        self.backButton.pack(side=RIGHT)
        self.deleteLivrableButton.pack(side=RIGHT)

    def createInfoFrame(self):
        fields = ["Nom", "Date Début", "Date Fin", "Budget", "Description"]
        row = 0

        for i in fields:

            entryLabel = Label(self.infoFrame, text=i)

            if "Date" in i:
                entry = DateEntry(self.infoFrame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, date_pattern='y-mm-dd', firstweekday='sunday')
            else:
                entry = Entry(self.infoFrame)

            entryLabel.grid(row=row, column=0, sticky=E + W)
            entry.grid(row=row, column=1, sticky=E + W)
            row += 1
            self.livrableInfo[i] = entry

    def createLibrableFrame(self):
        self.createLibrable = Button(
            self.buttonFrame, text="Créer", command=self.saveLivrable)
        self.backButton = Button(
            self.buttonFrame, text="Retour au menu", command=self.backToMenu)
        self.clearButton = Button(
            self.buttonFrame, text="Effacer", command=self.clearAllFields)
        self.createLibrable.pack(side=LEFT)
        self.clearButton.pack(side=LEFT)
        self.backButton.pack(side=RIGHT)

    def clearAllFields(self):
        self.livrableInfo["Nom"].delete(0, "end")
        self.livrableInfo["Budget"].delete(0, "end")
        self.livrableInfo["Description"].delete(0, "end")

        if self.messageLabel:
            self.messageLabel.destroy()

    def saveLivrable(self):
        #TODO valider budget numbers only

        self.livrableParam = self.getEntryData()

        if re.match(r"^[0-9.]*$", self.livrableParam["budget"]):
            self.parent.savelivrable(self.livrableParam)

        else:
            self.showMessage("Veuillez entrer un budget valide")

    def updateLivrable(self):
        self.livrableParam = self.getEntryData()
        self.livrableParam["id"] = self.livrable["id"]
        self.parent.updatelivrable(self.livrableParam)

    def getEntryData(self):
        param = {}
        param["nom"] = self.livrableInfo["Nom"].get()
        param["date_debut"] = self.livrableInfo["Date Début"].get_date()
        param["date_fin"] = self.livrableInfo["Date Fin"].get_date()
        param["budget"] = self.livrableInfo["Budget"].get()
        param["desc"] = self.livrableInfo["Description"].get()

        return param

    def backToMenu(self):
        self.livrableFrame.pack_forget()
        self.createModuleFrame()

    def deleteLivrable(self):
        livrableID = int(self.livrable["id"])
        
        self.parent.deleteLivrable(livrableID)

    def showMessage(self, reponseServeur):

        self.messageLabel = Label(self.confirmationFrame, text=reponseServeur)
        self.messageLabel.pack()

    def livrableDetails(self):

        selection = self.livrableList.get(self.livrableList.curselection())
        
        if selection != None:            
            for i in self.listeLivrables:
                if i[1] == selection:
                    
                    self.livrable["desc"] = i[1]
                    self.livrable["echeancier"] = self.parent.getEcheancier(i[2])                    
                    self.livrable["responsable"] = self.parent.getUser(i[3])
                    self.livrable["id"] = i[0]
                    

            self.gestionFrame.destroy()
            self.createDetailsFrame()
            self.createDetailsButtonFrame()
        else:
            print("Veuillez sélectionner un évènement")


class Modele():
    def __init__(self, parent):
        self.parent = parent

    def inscrireUser(self, args):
        self.user = {}
        self.username = args[2]
        self.userRole = args[1]
        self.courriel = args[3]


class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.connexion = Connexion()
        self.urlserveur = self.connexion.urlserveur
        self.modele.inscrireUser(sys.argv)
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def getUsername(self):
        return self.modele.username

    def getUserRole(self):
        return self.modele.userRole

    def getUserRole(self):
        return self.modele.courriel

    def saveLivrable(self, newlivrable):
        reponseServeur = self.connexion.saveLivrable(newlivrable)
        self.vue.showMessage(reponseServeur)

    def deleteLivrable(self, livrableID):
        reponseServeur = self.connexion.deleteLivrable(livrableID)
        self.vue.showMessage(reponseServeur)

    def getLivrables(self):
        return self.connexion.getLivrables(self.modele.courriel)

    def updatelivrable(self, updateData):
        reponseServeur = self.connexion.updateLivrable(updateData)
        self.vue.showMessage(reponseServeur)

    def getEcheancier(self, id):
        return self.connexion.populate("echeancier", id)

    def getUser(self, id):
        return self.connexion.populate("personnels", id)

    def appelserveur(self, route, params):
        return self.connexion.appelserveur(route, params)


if __name__ == '__main__':
    c = Controleur()
