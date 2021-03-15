from tkinter import *
from tkinter.ttk import *
import sys
import urllib.request
import urllib.parse

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

        self.eventParam["Nom"] = "test"
        self.eventParam["Date"] = "2020-03-15"
        self.eventParam["Budget"] = "1234"
        self.eventParam["Desc"] = "Allo"

        print(self.eventParam)
        self.parent.saveEvent(self.eventParam)



class Modele():

    def __init__(self, parent):
        self.parent = parent

    def saveEvent(self, newEvent):
        url = self.parent.urlserveur + "/newEvent"
        rep = self.parent.appelserveur(url, newEvent)
        repTxt =json.loads(rep)
        print(rep)


class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.urlserveur=sys.argv[1]
        self.vue.root.mainloop()

    def saveEvent(self, newEvent):

        self.modele.saveEvent(newEvent)

    def appelserveur(self,url,params):
        query_string = urllib.parse.urlencode( params )
        data = query_string.encode( "ascii" )
        url = url + "?" + query_string
        rep=urllib.request.urlopen(url , data)
        reptext=rep.read()
        return reptext
# def identifierusager(self,nom,mdp):
#         url = self.urlserveur+"/identifierusager"
#         params = {"nom":nom,
#                   "mdp":mdp}
#         reptext=self.appelserveur(url,params)

#         mondict=json.loads(reptext)
#         if "inconnu" in mondict:
#             self.vue.avertirusager("Inconnu","Reprendre?")
#         else:

#             self.modele.inscrireusager(mondict)
#             self.vue.creercadreprincipal(self.modele)
#             self.vue.changercadre("principal")






if __name__ == '__main__':
    c = Controleur()