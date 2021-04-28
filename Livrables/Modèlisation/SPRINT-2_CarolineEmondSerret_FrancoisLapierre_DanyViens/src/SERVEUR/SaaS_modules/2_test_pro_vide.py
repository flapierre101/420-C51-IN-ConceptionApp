from tkinter import *
from tkinter.ttk import *
import sys
import urllib.request
import urllib.parse
from flask import json

class Vue():
    def __init__(self,parent):
        self.parent=parent
        self.root=Tk()

        self.eventInfo = {}
        self.eventParam = {}
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

        fields = ["Nom", "Date Debut", "Date Fin", "Budget", "Description"]
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

        self.eventParam["Nom"] = self.eventInfo["Nom"].get()
        self.eventParam["Date_debut"] = self.eventInfo["Date Debut"].get()
        self.eventParam["Date_fin"] = self.eventInfo["Date Fin"].get()
        self.eventParam["Budget"] = self.eventInfo["Budget"].get()
        self.eventParam["Desc"] = self.eventInfo["Description"].get()

        # print(self.eventParam)
        self.parent.saveEvent(self.eventParam)



class Modele():

    def __init__(self, parent):
        self.parent = parent

    def saveEvent(self, newEvent):
        url = self.parent.urlserveur + "/newEvent"
        return self.parent.appelserveur(url, newEvent)

        # repTxt = json.loads(rep)
        # print(repTxt)


class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.urlserveur=sys.argv[1]
        self.vue.root.mainloop()

    def saveEvent(self, newEvent):
        url = self.urlserveur + "/newEvent"
        return self.appelserveur(url, newEvent)

    def appelserveur(self,url,params):
        query_string = urllib.parse.urlencode( params )
        data = query_string.encode( "ascii" )
        url = url + "?" + query_string
        rep=urllib.request.urlopen(url , data)
        reptext=rep.read()
        return reptext


if __name__ == '__main__':
    c = Controleur()