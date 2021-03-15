from tkinter import *
from tkinter.ttk import *
from tkcalendar import *


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.eventInfo = {}
        self.gestionFrame = Frame(self.root)
        self.createModuleFrame()

    def createModuleFrame(self):
        self.root.geometry("300x300")
        self.listFrame = Frame(self.gestionFrame)
        self.buttonFrame = Frame(self.gestionFrame)
        self.eventList = Listbox(self.listFrame)

        testEvents = ["Event1", "Event2", "Event3", "Event4"]
        row = 1

        for i in testEvents:
            self.eventList.insert(row, i)
            print(i)
            row += 1

        username = "Caroline"
        welcomeLabel = Label(self.root, text="Bienvenue " + username, font=("Arial", 14))
        title = Label(self.root, text="*** Gestion d'évènements ***", font=("Arial", 16))

        listLabel = Label(self.listFrame, text="Liste des évènements")
        listLabel.pack()
        self.eventList.pack()

        welcomeLabel.pack()
        title.pack()
        self.listFrame.pack(side=LEFT)

        self.createButtonFrame()
        self.buttonFrame.pack()
        self.gestionFrame.pack()

    def createButtonFrame(self):
        self.createEventButton = Button(self.buttonFrame, text="Créer un évènement", command=self.createNewEvent)
        self.eventDetailsButton = Button(self.buttonFrame, text="Détail de l'évènement")

        self.createEventButton.pack(fill=Y)
        self.eventDetailsButton.pack(fill=Y)

    def createNewEvent(self):
        self.gestionFrame.pack_forget()
        self.createEventFrame()


    def createEventFrame(self):
        self.root.geometry("300x300")
        self.eventFrame = Frame(self.root)
        self.infoFrame = Frame(self.eventFrame)
        self.buttonFrame = Frame(self.eventFrame)

        self.createInfoFrame()
        self.createEventButtonFrame()

        title = Label(self.eventFrame, text="* Créer un évènement *", font=("Arial", 14))
        title.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack()
        self.eventFrame.pack()


    def createInfoFrame(self):
        fields = ["Nom", "Date", "Budget", "Description"]
        row = 0
        for i in fields:
            entryLabel = Label(self.infoFrame, text=i)
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
        self.eventInfo["Date"].delete(0, "end")
        self.eventInfo["Budget"].delete(0, "end")
        self.eventInfo["Description"].delete(0, "end")

    def saveEvent(self):
        nom = self.eventInfo["Nom"].get()
        date = self.eventInfo["Date"].get()
        budget = self.eventInfo["Budget"].get()
        description = self.eventInfo["Description"].get()
        self.parent.saveEvent([nom, date, budget, description])

    def backToMenu(self):
        self.eventFrame.pack_forget()
        self.gestionFrame.pack()

    def showMessage(self, reponseServeur):
        self.confirmationFrame = Frame(self.eventFrame)
        messageLabel = Label(self.confirmationFrame, text=reponseServeur)
        messageLabel.pack()
        self.confirmationFrame.pack(pady=10)


class Modele():
    def __init__(self, parent):
        self.parent = parent

    def saveEvent(self, newEvent):
        pass


class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def saveEvent(self, newEvent):
        #reponseServeur = self.modele.saveEvent(newEvent)
        #self.vue.showMessage(responseServeur)
        self.modele.saveEvent(newEvent)
        reponseServeur = "Nouvel évènement enregistré"
        self.vue.showMessage(reponseServeur)



if __name__ == '__main__':
    c = Controleur()
