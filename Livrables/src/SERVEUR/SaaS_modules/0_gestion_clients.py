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
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connexion import *

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.clientInfo = {}
        self.welcomeLabel = Label(self.root, text="Bienvenue ", font=("Arial", 14)).pack()
        self.title = Label(self.root, text="*** Gestion des Clients ***", font=("Arial", 16)).pack()
        self.createModuleFrame()

    def createModuleFrame(self):
        self.gestionFrame = Frame(self.root)
        # self.listeclients = self.parent.getEvent() #TODO changer pour client
        self.root.geometry("1000x800")
        self.listFrame = Frame(self.gestionFrame)
        self.buttonFrame = Frame(self.gestionFrame)
        self.clientsTableau = Treeview(self.gestionFrame, show = 'headings')

        # for i in range(len(self.listeclients)):
        #     self.clientsTableau.insert(i, self.listeclients[0])
        self.clientsTableau["column"] = ("ID", "Nom", "Courriel", "Téléphone", "Compagnie", "Adresse", "Rue", "Ville")
        self.clientsTableau.column("ID", width=50)
        self.clientsTableau.column("Nom", width=100)
        self.clientsTableau.column("Courriel", width=100)
        self.clientsTableau.column("Téléphone", width=100)
        self.clientsTableau.column("Compagnie", width=100)
        self.clientsTableau.column("Adresse", width=100)
        self.clientsTableau.column("Rue", width=100)
        self.clientsTableau.column("Ville", width=100)

        self.clientsTableau.heading("ID",text="ID")
        self.clientsTableau.heading("Nom",text="Nom")
        self.clientsTableau.heading("Courriel",text="Courriel")
        self.clientsTableau.heading("Téléphone",text="Téléphone")
        self.clientsTableau.heading("Compagnie",text="Compagnie")
        self.clientsTableau.heading("Adresse",text="Adresse")
        self.clientsTableau.heading("Rue",text="Rue")
        self.clientsTableau.heading("Ville",text="Ville")

        # TODO for loop de insert des clients et mettre des tags
        # self.clientsTableau.tag_configure('oddrow', background='orange')
        listLabel = Label(self.listFrame, text="Liste des Clients")
        listLabel.pack()
        self.clientsTableau.pack(side=TOP)

        self.listFrame.pack(side=LEFT)

        self.createButtonFrame()
        self.buttonFrame.pack()
        self.gestionFrame.pack()

    def createButtonFrame(self):
        self.createClientButton = Button(self.buttonFrame, width=25, text="Nouveau Client", command=self.create_client)
        self.clientDetailsButton = Button(self.buttonFrame, width=25, text="Modifier le Client")
        self.suppClientButton = Button(self.buttonFrame, width=25, text="Supprimer le Client")

        self.createClientButton.pack(fill=Y)
        self.clientDetailsButton.pack(fill=Y)
        self.suppClientButton.pack(fill=Y)

    def create_client(self):
        self.gestionFrame.destroy()
        self.create_client_frame()

    def create_client_frame(self):
        self.root.geometry("1000x800")
        self.clientFrame = Frame(self.root)
        self.infoFrame = Frame(self.clientFrame)
        self.buttonFrame = Frame(self.clientFrame)
        self.confirmationFrame = Frame(self.clientFrame)

        self.createInfoFrame()
        self.createClientButtonFrame()

        title = Label(self.clientFrame, text="* Créer un Client *", font=("Arial", 14))
        title.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack()
        self.clientFrame.pack()
        self.confirmationFrame.pack(pady=10)

    def createInfoFrame(self):
        fields = ["ID", "Nom", "Courriel", "Téléphone", "Compagnie", "Adresse", "Rue", "Ville"]

        for i in range (len(fields)):
            entryLabel = Label(self.infoFrame, text=fields[i], width=25)

            entry = Entry(self.infoFrame)

            entryLabel.grid(row=i, column=0, sticky=E+W)
            entry.grid(row=i, column=1, sticky=E+W)
            self.clientInfo[fields[i]] = entry
    def createClientButtonFrame(self):

        # self.updateEventButton = Button(self.buttonFrame, text="Modifier", command=self.updateEvent)
        self.backButton = Button(self.buttonFrame, text="Retour au menu", command=self.backToMenu)
        self.deleteEventButton = Button(self.buttonFrame, text="Supprimer l'évènement")
        # self.updateEventButton.pack(side=LEFT)
        self.backButton.pack(side=RIGHT)
        self.deleteEventButton.pack(side=RIGHT)

    def backToMenu(self):
        self.clientFrame.pack_forget()
        self.createModuleFrame()

    def modif_client_frame(self):
        pass

    def clearAllFields(self):
        pass

    def save_client(self):
        pass

    def update_client(self):
        pass

    def getEntryData(self):
        param = {}
        #return param
        pass

    def delete_client(self):
        pass

    def showMessage(self, reponseServeur):
        pass

    def client_details(self):
        pass



class Modele():
    def __init__(self, parent):
        self.parent = parent

class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.connexion = Connexion()
        self.urlserveur = self.connexion.urlserveur
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def get_client(self):
        pass
        # return self.connexion.getClient()

    def save_client(self):
        pass

    def delete_client(self):
        pass

    def update_client(self):
        pass

    def appelserveur(self, rout, params):
        pass


if __name__ == '__main__':
    c = Controleur()