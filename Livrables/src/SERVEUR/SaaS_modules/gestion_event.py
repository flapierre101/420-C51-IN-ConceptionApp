from tkinter import *
from tkinter.ttk import *

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.createModuleFrame()


    def createModuleFrame(self):
        self.root.geometry("300x300")
        self.listFrame = Frame(self.root)
        self.buttonFrame = Frame(self.root)
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

    def createButtonFrame(self):

        self.createEventButton = Button(self.buttonFrame, text="Créer un évènement")
        self.eventDetailsButton = Button(self.buttonFrame, text="Détail de l'évènement")

        self.createEventButton.pack(fill=Y)
        self.eventDetailsButton.pack(fill=Y)





class Modele():
    def __init__(self, parent):
        self.parent = parent


class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.vue.root.mainloop()


if __name__ == '__main__':
    c = Controleur()
