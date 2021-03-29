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
# import ../connexion.py
from connexion import *

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.eventInfo = {}
        self.event = {}
        self.eventParam = {}
        self.messageLabel = None
        username = "Caroline"
        self.welcomeLabel = Label(self.root, text="Bienvenue " + username, font=("Arial", 14)).pack()
        self.title = Label(self.root, text="*** Gestion d'évènements ***", font=("Arial", 16)).pack()
        self.createModuleFrame()

    def createModuleFrame(self):
        self.gestionFrame = Frame(self.root)
        self.listeprojets = self.parent.getEvent()
        self.root.geometry("300x300")
        self.listFrame = Frame(self.gestionFrame)
        self.buttonFrame = Frame(self.gestionFrame)
        self.eventList = Listbox(self.listFrame)

        row = 1

        for i in self.listeprojets:
            self.eventList.insert(row, i[0])
            row += 1

        listLabel = Label(self.listFrame, text="Liste des évènements")
        listLabel.pack()
        self.eventList.pack()

        self.listFrame.pack(side=LEFT)

        self.createButtonFrame()
        self.buttonFrame.pack()
        self.gestionFrame.pack()

    def createButtonFrame(self):
        self.createEventButton = Button(self.buttonFrame, text="Créer un évènement", command=self.createNewEvent)
        self.eventDetailsButton = Button(self.buttonFrame, text="Détail de l'évènement", command=self.eventDetails)
        #self.eventPersonnelButton = Button(self.buttonFrame, text="Employés de ")

        self.createEventButton.pack(fill=Y)
        self.eventDetailsButton.pack(fill=Y)

    def createNewEvent(self):
        self.gestionFrame.destroy()
        self.createEventFrame()


    def createEventFrame(self):
        self.root.geometry("300x300")
        self.eventFrame = Frame(self.root)
        self.infoFrame = Frame(self.eventFrame)
        self.buttonFrame = Frame(self.eventFrame)
        self.confirmationFrame = Frame(self.eventFrame)

        self.createInfoFrame()
        self.createEventButtonFrame()

        title = Label(self.eventFrame, text="* Créer un évènement *", font=("Arial", 14))
        title.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack()
        self.eventFrame.pack()
        self.confirmationFrame.pack(pady=10)

    def createDetailsFrame(self):
        self.root.geometry("300x300")
        self.eventFrame = Frame(self.root)
        self.infoFrame = Frame(self.eventFrame)
        self.buttonFrame = Frame(self.eventFrame)
        self.confirmationFrame = Frame(self.eventFrame)

        self.createInfoDetailsFrame()

        title = Label(self.eventFrame, text="* Modifier un évènement *", font=("Arial", 14))
        title.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack()
        self.eventFrame.pack()
        self.confirmationFrame.pack(pady=10)

    def createInfoDetailsFrame(self):
        fields = ["Nom", "Date Début", "Date Fin", "Budget", "Description"]
        row = 0

        for i in fields:

            entryLabel = Label(self.infoFrame, text=i)

            if "Nom" in i:
                entry = Entry(self.infoFrame)
                entry.insert(0,self.event["nom"])
            elif "Date Début" in i:
                entry = DateEntry(self.infoFrame, width=12, background='darkblue',
                                foreground='white', borderwidth=2, date_pattern='y-mm-dd', firstweekday='sunday')
                entry.set_date(self.event["date_debut"])
            elif "Date Fin" in i:
                entry = DateEntry(self.infoFrame, width=12, background='darkblue',
                                foreground='white', borderwidth=2, date_pattern='y-mm-dd', firstweekday='sunday')
                entry.set_date(self.event["date_fin"])
            elif "Budget" in i:
                entry = Entry(self.infoFrame)
                entry.insert(0,self.event["budget"])
            else:
                entry = Entry(self.infoFrame)
                entry.insert(0, self.event["desc"])

            entryLabel.grid(row=row, column=0, sticky=E + W)
            entry.grid(row=row, column=1, sticky=E + W)
            row += 1
            self.eventInfo[i] = entry

    def createDetailsButtonFrame(self):
        self.updateEventButton = Button(self.buttonFrame, text="Modifier", command=self.updateEvent)
        self.backButton = Button(self.buttonFrame, text="Retour au menu", command=self.backToMenu)
        self.updateEventButton.pack(side=LEFT)
        self.backButton.pack(side=RIGHT)


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
            self.eventInfo[i] = entry


    def createEventButtonFrame(self):
        self.createEventButton = Button(self.buttonFrame, text="Créer", command=self.saveEvent)
        self.backButton = Button(self.buttonFrame, text="Retour au menu", command=self.backToMenu)
        self.clearButton = Button(self.buttonFrame, text="Effacer", command=self.clearAllFields)
        self.createEventButton.pack(side=LEFT)
        self.clearButton.pack(side=LEFT)
        self.backButton.pack(side=RIGHT)

    def clearAllFields(self):
        self.eventInfo["Nom"].delete(0, "end")
        self.eventInfo["Date Début"].set_date(datetime.date.today())
        self.eventInfo["Date Fin"].set_date(datetime.date.today())
        self.eventInfo["Budget"].delete(0, "end")
        self.eventInfo["Description"].delete(0, "end")

        if self.messageLabel:
            self.messageLabel.destroy()

    def saveEvent(self):
        #TODO valider budget numbers only

        self.eventParam = self.getEntryData()

        if re.match(r"^[0-9.]*$", self.eventParam["budget"]):
            self.parent.saveEvent(self.eventParam)

        else:
            self.showMessage("Veuillez entrer un budget valide")

    def updateEvent(self):
        self.eventParam = self.getEntryData()
        self.eventParam["id"] = self.event["id"]
        self.parent.updateEvent(self.eventParam)

    def getEntryData(self):
        param = {}
        param["nom"] = self.eventInfo["Nom"].get()
        param["date_debut"] = self.eventInfo["Date Début"].get_date()
        param["date_fin"] = self.eventInfo["Date Fin"].get_date()
        param["budget"] = self.eventInfo["Budget"].get()
        param["desc"] = self.eventInfo["Description"].get()

        return param


    def backToMenu(self):
        self.eventFrame.pack_forget()
        self.createModuleFrame()

    def showMessage(self, reponseServeur):

        self.messageLabel = Label(self.confirmationFrame, text=reponseServeur)
        self.messageLabel.pack()

    def eventDetails(self):

        selection = self.eventList.get(self.eventList.curselection())

        if selection != None:

            for i in self.listeprojets:
                if i[0] == selection:
                    self.event["nom"] = i[0]
                    self.event["date_debut"] = i[1]
                    self.event["date_fin"] = i[2]
                    self.event["budget"] = i[3]
                    self.event["desc"] = i[4]
                    self.event["id"] = i[5]
                    print("print ln 218", self.event)


            self.gestionFrame.destroy()
            self.createDetailsFrame()
            self.createDetailsButtonFrame()
        else:
            print("Veuillez sélectionner un évènement")




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

    def saveEvent(self, newEvent):
        reponseServeur = self.connexion.saveEvent(newEvent)
        self.vue.showMessage(reponseServeur)

    def getEvent(self):
        return self.connexion.getEvent()

    def updateEvent(self, updateData):
        reponseServeur = self.connexion.updateEvent(updateData)
        self.vue.showMessage(reponseServeur)

    def appelserveur(self,route,params):
        return self.connexion.appelserveur(route,params)



if __name__ == '__main__':
    c = Controleur()
