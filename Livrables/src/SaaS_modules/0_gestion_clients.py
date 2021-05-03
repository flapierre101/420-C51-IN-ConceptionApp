from tkinter import *
from tkinter.ttk import *
from tkcalendar import *
import urllib.parse
from flask import json
import sys

# à copier dans chaque nouveau module pour avoir la classe connexion
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connexion import *

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.root.title("Production CDJ - Réunions")
        self.clientInfo = {}
        self.listeclients = self.parent.getClients()
        self.welcomeLabel = Label(self.root, text="Bienvenue ", font=("Arial", 14)).pack()
        self.title = Label(self.root, text="*** Gestion des Clients ***", font=("Arial", 16)).pack()
        self.maxClient = Label(self.root, text="Client: "+str(len(self.listeclients))+"/"+str(self.parent.getMaxClient()) , font=("Arial", 12)).pack()
        self.createModuleFrame()
        # self.confirmationFrame = None

    def createModuleFrame(self):
        self.gestionFrame = Frame(self.root)
        self.root.geometry("1000x800")
        self.listFrame = Frame(self.gestionFrame)
        self.buttonFrame = Frame(self.gestionFrame)
        self.clientsTableau = Treeview(self.gestionFrame, show = 'headings')
        self.confirmationFrame = Frame(self.gestionFrame)


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

        tempo = 'odd'
        for i in range(len(self.listeclients)):
            if tempo == 'odd':
                self.clientsTableau.insert('', 'end', text=self.listeclients[i][0], values=self.listeclients[i][0:], tag='odd')
                tempo ='event'
            else:

                self.clientsTableau.insert('', 'end', text=self.listeclients[i][0], values=self.listeclients[i][0:], tag='event')
                tempo ='odd'

        # Not working ATM
        # self.clientsTableau.tag_configure('odd', background='Black', foreground='White')
        # self.clientsTableau.tag_configure('event', background='White', foreground='Black')

        listLabel = Label(self.listFrame, text="Liste des Clients")
        listLabel.pack(side=TOP)
        self.clientsTableau.pack(side=TOP)

        self.listFrame.pack(side=LEFT)

        self.createButtonFrame()
        self.buttonFrame.pack()
        self.gestionFrame.pack()
        self.confirmationFrame.pack(pady=10, anchor=S)

    def createButtonFrame(self):
        self.createClientButton = Button(self.buttonFrame, width=25, text="Nouveau Client", command=self.create_client)
        self.clientDetailsButton = Button(self.buttonFrame, width=25, text="Modifier le Client", command=self.modifier_client)
        self.suppClientButton = Button(self.buttonFrame, width=25, text="Supprimer le Client", command=self.delete_client)

        self.createClientButton.grid(column=0, row=0, pady=5, padx=5)
        self.clientDetailsButton.grid(column=1, row=0, pady=5, padx=5)
        self.suppClientButton.grid(column=2, row=0, pady=5, padx=5)

    def create_client(self):
        self.gestionFrame.destroy()
        if self.parent.verif():
            self.create_client_frame()

        else:
            self.showMessage("Vous avez atteind le votre maximum de client.")

    def create_client_frame(self):
        self.root.geometry("1000x800")
        self.clientFrame = Frame(self.root)
        self.infoFrame = Frame(self.clientFrame)
        self.buttonFrame = Frame(self.clientFrame)
        self.confirmationFrame = Frame(self.clientFrame)
        self.clientMinMax = Label(self.confirmationFrame, text=len(self.getClients()))

        self.createInfoFrame()
        self.createClientButtonFrame()

        title = Label(self.clientFrame, text="* Créer un Client *", font=("Arial", 14))
        title.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack()
        self.clientFrame.pack()
        self.confirmationFrame.pack(pady=10)

    def modifier_client(self):
        # self.gestionFrame.destroy()
        self.gestionFrame.pack_forget()
        self.modif_client_frame()

    def modif_client_frame(self):
        self.root.geometry("1000x800")
        self.clientFrame = Frame(self.root)
        self.infoFrame = Frame(self.clientFrame)
        self.buttonFrame = Frame(self.clientFrame)
        self.confirmationFrame = Frame(self.clientFrame)

        itemsTableau = self.clientsTableau.selection()

        self.createInfoFrame(self.clientsTableau.item(itemsTableau)['values'])
        self.modifClientButtonFrame()

        title = Label(self.clientFrame, text="* Modifier un Client *", font=("Arial", 14))
        title.pack()
        self.clientFrame.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack()
        self.confirmationFrame.pack(pady=10)

    def createInfoFrame(self, selection=None):
        fields = ["ID", "Nom", "Courriel", "Téléphone", "Compagnie", "Adresse", "Rue", "Ville"]
        for i in range (len(fields)):
            entryLabel = Label(self.infoFrame, text=fields[i], width=25)

            entry = Entry(self.infoFrame)

            if selection is not None:
                entry.insert(0,selection[i])
                # entry.insert(0, "placeholder")
            if fields[i] == "ID":
                entry.configure(state=DISABLED)

            entryLabel.grid(row=i, column=0, sticky=E+W)
            entry.grid(row=i, column=1, sticky=E+W)
            self.clientInfo[fields[i]] = entry


    def createClientButtonFrame(self):
        self.newClientButton = Button(self.buttonFrame, text="Ajouter", command=self.save_client)
        self.backButton = Button(self.buttonFrame, text="Retour au menu", command=self.backToMenu)
        self.newClientButton.pack(side=LEFT)
        self.backButton.pack(side=RIGHT)

    def modifClientButtonFrame(self):
        self.updateClientButton = Button(self.buttonFrame, text="Modifier", command=self.update_client)
        self.backButton = Button(self.buttonFrame, text="Retour au menu", command=self.backToMenu)
        self.updateClientButton.pack(side=LEFT)
        self.backButton.pack(side=RIGHT)


    def backToMenu(self):
        self.clientFrame.pack_forget()
        self.createModuleFrame()

    def clearAllFields(self):
        pass

    def save_client(self):
        self.clientInfo = self.getEntryData()
        self.parent.save_client(self.clientInfo)
        self.backToMenu()


    def update_client(self):
        self.clientInfo = self.getEntryData()
        self.parent.update_client(self.clientInfo)
        self.backToMenu()

    def getEntryData(self):
        param = {}
        param["nom"] = self.clientInfo["Nom"].get()
        param["courriel"] = self.clientInfo["Courriel"].get()
        param["telephone"] = self.clientInfo["Téléphone"].get()
        param["compagnie"] = self.clientInfo["Compagnie"].get()
        param["adresse"] = self.clientInfo["Adresse"].get()
        param["rue"] = self.clientInfo["Rue"].get()
        param["ville"] = self.clientInfo["Ville"].get()
        param["idclient"] = self.clientInfo["ID"].get()
        return param

    def delete_client(self):
        clientId = ""
        for _id in self.clientsTableau.selection():
            clientId = self.clientsTableau.item(_id,"text")

        self.parent.delete_client(clientId)
        self.gestionFrame.pack_forget()
        self.createModuleFrame()


    def showMessage(self, reponseServeur):
        self.messageLabel = Label(self.confirmationFrame, text=reponseServeur)
        self.messageLabel.pack(side=BOTTOM)


class Modele():
    def __init__(self, parent):
        self.parent = parent

    def verif (self):
        forfait = self.userInfo['forfait']
        nbclient = len(self.getClients());
        if (forfait == 1 and nbclient <= 1) or (forfait == 2 and nbclient <= 1500) or (forfait == 3 and nbclient < 1):
            return True
        else:
            return False



class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.connexion = Connexion()
        self.urlserveur = self.connexion.urlserveur
        self.userInfo = json.loads(sys.argv[4])
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def getClients(self):
        return self.connexion.getClients()


    def save_client(self, clientData):
        reponseServeur = self.connexion.save_client(clientData)
        self.vue.showMessage(reponseServeur)


    def delete_client(self, clientId):
        reponseServeur = self.connexion.delete_client(clientId)
        self.vue.showMessage(reponseServeur)

    def update_client(self, updatedData):
        reponseServeur = self.connexion.updateClient(updatedData)
        reponseServeur = str(reponseServeur)
        print("***********************LA REPONSE:  ", type(reponseServeur))
        self.vue.showMessage(reponseServeur)

    def appelserveur(self, route, params):
        return self.connexion.appelserveur(route, params)

    def getMaxClient(self):
        reponseServeur = self.connexion.getMaxClient(self.userInfo['forfait'])

        self.vue.showMessage(reponseServeur)

    def verif(self):
        return Modele.verif(self)

#TODO AJOUT DE CMPTE DU NB DE CLIENTS DANS LA BD

if __name__ == '__main__':
    c = Controleur()