from tkinter import *
from tkinter.ttk import *
from tkcalendar import *
from flask import json
import sys
# à copier dans chaque nouveau module pour avoir la classe connexion
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connexion import *


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.root.tk.call('lappend', 'auto_path', './Styles/awthemes-10.3.0')
        # Dark theme
        self.root.tk.call('package', 'require', 'awdark')
        # Light theme
        self.root.tk.call('package', 'require', 'awlight')
        self.style = Style(self.root)
        self.style.theme_use("awlight")
        # self.root.configure(bg='#33393b')
        self.root.configure(bg='#e8e8e7')
        self.root.title("Production CDJ - Clients")
        self.clientInfo = {}
        self.listeclients = self.parent.getClients()
        self.maxClient = self.parent.getMaxClient()
        self.welcomeLabel = Label(
            self.root, text="Bienvenue " + self.parent.getUsername(), font=("Arial", 14)).pack(pady=10)
        self.title = Label(
            self.root, text="*** Gestion des Clients ***", font=("Arial", 16)).pack(pady=5)
        self.createModuleFrame()

    def createModuleFrame(self):
        self.gestionFrame = Frame(self.root)
        self.root.geometry("900x600")
        self.listFrame = Frame(self.gestionFrame)
        self.buttonFrame = Frame(self.gestionFrame)
        self.clientsTableau = Treeview(self.gestionFrame, show='headings')
        self.confirmationFrame = Frame(self.gestionFrame)
        self.listeclients = self.parent.getClients()
        self.maxClientLabel = Label(self.gestionFrame, text="Client: "+str(
            len(self.listeclients))+"/"+str(self.maxClient), font=("Arial", 12)).pack(pady=10)

        self.clientsTableau["column"] = (
            "ID", "Nom", "Courriel", "Téléphone", "Compagnie", "Adresse", "Rue", "Ville")
        self.clientsTableau.column("ID", width=50)
        self.clientsTableau.column("Nom", width=100)
        self.clientsTableau.column("Courriel", width=100)
        self.clientsTableau.column("Téléphone", width=100)
        self.clientsTableau.column("Compagnie", width=100)
        self.clientsTableau.column("Adresse", width=100)
        self.clientsTableau.column("Rue", width=100)
        self.clientsTableau.column("Ville", width=100)

        self.clientsTableau.heading("ID", text="ID")
        self.clientsTableau.heading("Nom", text="Nom")
        self.clientsTableau.heading("Courriel", text="Courriel")
        self.clientsTableau.heading("Téléphone", text="Téléphone")
        self.clientsTableau.heading("Compagnie", text="Compagnie")
        self.clientsTableau.heading("Adresse", text="Adresse")
        self.clientsTableau.heading("Rue", text="Rue")
        self.clientsTableau.heading("Ville", text="Ville")

        tempo = 'odd'
        for i in range(len(self.listeclients)):
            if tempo == 'odd':
                self.clientsTableau.insert(
                    '', 'end', text=self.listeclients[i][0], values=self.listeclients[i][0:], tags=("odd", "1"))
                tempo = 'event'
            else:
                self.clientsTableau.insert(
                    '', 'end', text=self.listeclients[i][0], values=self.listeclients[i][0:], tags=("event", "2"))
                tempo = 'odd'

        self.clientsTableau.tag_configure(
            "odd", background='Gray', foreground='White')
        self.clientsTableau.tag_configure(
            "event", background='Lightgray', foreground='Black')
        self.clientsTableau.pack(side=TOP)
        self.listFrame.pack(side=LEFT)

        self.createButtonFrame()
        self.buttonFrame.pack()
        self.gestionFrame.pack()
        self.confirmationFrame.pack(pady=10, anchor=S)

    def createButtonFrame(self):
        self.createClientButton = Button(
            self.buttonFrame, width=25, text="Nouveau Client", command=self.create_client)
        self.clientDetailsButton = Button(
            self.buttonFrame, width=25, text="Modifier le Client", command=self.modifier_client)
        self.suppClientButton = Button(
            self.buttonFrame, width=25, text="Supprimer le Client", command=self.delete_client)

        self.createClientButton.grid(column=0, row=0, pady=5, padx=5)
        self.clientDetailsButton.grid(column=1, row=0, pady=5, padx=5)
        self.suppClientButton.grid(column=2, row=0, pady=5, padx=5)

    def create_client(self):
        if self.maxClient > len(self.listeclients):
            self.gestionFrame.forget()
            self.create_client_frame()

        else:
            self.showMessage("Vous avez atteind le votre maximum de client.")

    def create_client_frame(self):
        self.root.geometry("1000x800")
        self.clientFrame = Frame(self.root)
        self.infoFrame = Frame(self.clientFrame)
        self.buttonFrame = Frame(self.clientFrame)
        self.confirmationFrame = Frame(self.clientFrame)

        self.createInfoFrame()
        self.createClientButtonFrame()

        title = Label(self.clientFrame,
                      text="* Créer un Client *", font=("Arial", 14))
        title.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack(pady=20)
        self.clientFrame.pack()
        self.confirmationFrame.pack(pady=10)

    def modifier_client(self):
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

        title = Label(self.clientFrame,
                      text="* Modifier un Client *", font=("Arial", 14))
        title.pack()
        self.clientFrame.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack()
        self.confirmationFrame.pack(pady=10)

    def createInfoFrame(self, selection=None):
        fields = ["ID", "Nom", "Courriel", "Téléphone",
                  "Compagnie", "Adresse", "Rue", "Ville"]
        for i in range(len(fields)):
            entryLabel = Label(self.infoFrame, text=fields[i], width=25)

            entry = Entry(self.infoFrame)
            if selection is not None:
                if len(selection) != 0:
                    entry.insert(0, selection[i])
                else:
                    return self.showMessage("Selectionez un client à modifier")
            if fields[i] == "ID":
                entry.configure(state=DISABLED)

            entryLabel.grid(row=i, column=0, sticky=E+W, pady=3)
            entry.grid(row=i, column=1, sticky=E+W)
            self.clientInfo[fields[i]] = entry

    def createClientButtonFrame(self):
        self.newClientButton = Button(
            self.buttonFrame, text="Ajouter", command=self.save_client)
        self.backButton = Button(
            self.buttonFrame, text="Retour au menu", command=self.backToMenu)
        self.newClientButton.pack(side=LEFT, padx=5)
        self.backButton.pack(side=RIGHT, padx=5)

    def modifClientButtonFrame(self):
        self.updateClientButton = Button(
            self.buttonFrame, text="Modifier", command=self.update_client)
        self.backButton = Button(
            self.buttonFrame, text="Retour au menu", command=self.backToMenu)
        self.updateClientButton.pack(side=LEFT, pady=20, padx=5)
        self.backButton.pack(side=RIGHT, pady=20, padx=5)

    def backToMenu(self):
        self.clientFrame.pack_forget()
        self.createModuleFrame()

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
            clientId = self.clientsTableau.item(_id, "text")

        self.parent.delete_client(clientId)
        self.gestionFrame.pack_forget()
        self.createModuleFrame()

    def showMessage(self, reponseServeur):
        self.messageLabel = Label(self.confirmationFrame, text=reponseServeur)
        self.messageLabel.pack(side=BOTTOM)


class Modele():
    def __init__(self, parent):
        self.parent = parent


class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.connexion = Connexion()
        self.userInfo = json.loads(sys.argv[4])
        self.vue = Vue(self)
        self.vue.root.mainloop()
        self.urlserveur = self.connexion.urlserveur

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
        self.vue.showMessage(reponseServeur)

    def appelserveur(self, route, params):
        return self.connexion.appelserveur(route, params)

    def getMaxClient(self):
        return self.connexion.getMaxClient(self.userInfo['forfait'])

    def getUsername(self):
        self.username = sys.argv[2]
        return self.username


if __name__ == '__main__':
    c = Controleur()
