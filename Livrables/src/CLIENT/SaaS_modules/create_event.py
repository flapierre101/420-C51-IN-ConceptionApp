from tkinter import *
from tkinter.ttk import *

class Vue():
    def __init__(self,parent):
        self.parent=parent
        self.root=Tk()

        self.eventInfo = {}
        self.createEventFrame()

    def createEventFrame(self):
        self.root.geometry("200x200")
        self.infoFrame = Frame(self.root)
        self.buttonFrame = Frame(self.root)
        #self.confirmationFrame = Frame(self.root)

        self.createInfoFrame()
        self.createButtonFrame()

        title = Label(self.root, text="* Créer un évènement *", font=("Arial", 14))
        title.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack()

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

    def createButtonFrame(self):

        self.createEventButton = Button(self.buttonFrame, text="Enregistrer", command=self.saveEvent)
        self.createEventButton.pack(side=LEFT)

    def saveEvent(self):

        nom = self.eventInfo["Nom"].get()
        date =self.eventInfo["Date"].get()
        budget = self.eventInfo["Budget"].get()
        description = self.eventInfo["Description"].get()

        print("ENREGISTRER: ", nom, date, budget, description)
        self.parent.saveEvent([nom, date, budget, description])



class Modele():

    def __init__(self, parent):
        self.parent = parent
        self.listecours = []

    def saveEvent(self, newEvent):
        pass


class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def saveEvent(self, newEvent):

        self.modele.saveEvent(newEvent)






if __name__ == '__main__':
    c = Controleur()