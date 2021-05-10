
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
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
        self.root.title("Production CDJ - Livrables")
        self.livrableParam = {}
        self.messageLabel = None
        self.welcomeLabel = Label(
            self.root, text="Bienvenue " + self.parent.getUsername(), font=("Arial", 14)).pack()
        self.title = Label(
            self.root, text="*** Gestion des livrables ***", font=("Arial", 16)).pack()
        self.listeComplete = 0
        self.createModuleFrame()
        self.dontcreate = True

    def createModuleFrame(self):
        self.gestionFrame = Frame(self.root)
        self.listeLivrables = self.parent.getLivrables(self.listeComplete)
        self.root.geometry("500x325")
        self.listFrame = Frame(self.gestionFrame)
        self.buttonFrame = Frame(self.gestionFrame)
        self.livrableList = Listbox(self.listFrame, width=30)

        row = 1        
        for i in self.listeLivrables:
            self.livrableList.insert(row, i[1])
            row += 1
        text = "Livrables assignés incomplets" if self.listeComplete == 0 else "Livrables assignés complétés"
        listLabel = Label(self.listFrame, text=text)
        listLabel.pack()
        self.livrableList.pack()

        self.listFrame.pack(side=LEFT)  
        self.livrableInfo = {}
        self.indexEventSelect = None
        self.indexEcheancierSelect = None
        
        self.createButtonFrame()
        self.buttonFrame.pack()
        self.gestionFrame.pack()

    def createDetailsButtonFrame(self):
        text = "Compléter" if self.livrable["status"] == "Incomplet" else "À faire"
        self.updatelivrableButton = Button(
            self.buttonFrame, text=text, command=self.completeLivrable)
        self.updateNotes = Button(
            self.buttonFrame, text="Enregistrer notes", command=self.updateLivrables)
        self.backButton = Button(
            self.buttonFrame, text="Retour au menu", command=self.backToMenu)
        self.updatelivrableButton.pack(side=LEFT)
        self.updateNotes.pack(side=LEFT)
        self.backButton.pack(side=RIGHT)

    def createButtonFrame(self):
        self.livrableDetailButton = Button(
            self.buttonFrame, text="Détail du livrable", command=self.livrableDetails)

        self.createAddButton = Button(self.buttonFrame, text="Ajouter un livrable",command=self.createNewLivrable)
        if self.listeComplete == 0:            
            self.showcompletebtn = Button(
                self.buttonFrame, text="Afficher livrables completés", command=self.invertLivrableList)
        else:            
            self.showcompletebtn = Button(
                self.buttonFrame, text="Afficher livrables incomplets", command=self.invertLivrableList)
        self.livrableDetailButton.pack(fill=Y)
        self.createAddButton .pack(fill=Y)
        self.showcompletebtn.pack(fill=Y)

    def invertLivrableList(self):
        self.listeComplete = 0 if self.listeComplete == 1 else 1
        self.gestionFrame.pack_forget()
        self.createModuleFrame()

    def createDetailsFrame(self):
        self.root.geometry("500x325")
        self.livrableFrame = Frame(self.root)
        self.infoFrame = Frame(self.livrableFrame)
        self.buttonFrame = Frame(self.livrableFrame)
        self.confirmationFrame = Frame(self.livrableFrame)

        self.createInfoDetailsFrame()

        title = Label(self.livrableFrame,
                      text="* Détail du livrable *", font=("Arial", 14))
        title.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack()
        self.livrableFrame.pack()
        self.confirmationFrame.pack(pady=10)

    def createInfoDetailsFrame(self):
        fields = ["Titre","État", "Propriétaire", "Échéancier associé", "Date Limite", "Notes"]
        row = 0
        #print(self.parent.getUserRole())
        for i in fields:

            entryLabel = Label(self.infoFrame, text=i)

            if "Titre" in i:
                entry = Entry(self.infoFrame)
                entry.insert(0, self.livrable["desc"])
            elif "État" in i:
                entry = Entry(self.infoFrame)
                entry.insert(0, self.livrable["status"])
            elif "Propriétaire" in i:
                entry = Entry(self.infoFrame, width=60)
                entry.insert(0, self.livrable["responsable"][3] + " " + self.livrable["responsable"][2])
            elif "Échéancier associé" in i:
                entry = Entry(self.infoFrame)
                entry.insert(0, self.livrable["echeancier"][1])
            elif "Date Limite" in i:
                entry = DateEntry(self.infoFrame, width=12, background='darkblue',
                foreground='white', borderwidth=2, date_pattern='y-mm-dd', firstweekday='sunday')
                entry.set_date(self.livrable["echeancier"][2])                     
            elif "Notes" in i:                
                entry = scrolledtext.ScrolledText(self.infoFrame, width=15, height=6)                        
                entry.insert(END, self.livrable["notes"])
                

            if not "Notes" in i:
                entry.config(state='disabled')


            entryLabel.grid(row=row, column=0, sticky=E + W)
            entry.grid(row=row, column=1, sticky=E + W)
            row += 1
            self.livrableInfo[i] = entry
        text = self.livrableInfo["Notes"].get("1.0",END).strip()

    def createNewLivrable(self):
        self.gestionFrame.destroy()
        self.addLivrableFrame()
    
    def addLivrableFrame(self):
        self.root.geometry("450x450")
        self.livrableFrame = Frame(self.root)
        self.infoFrame = Frame(self.livrableFrame)
        self.buttonFrame = Frame(self.livrableFrame)
        self.confirmationFrame = Frame(self.livrableFrame)

        self.createLivrableFrame()
        self.createLivrableButtonFrame()

        title = Label(self.livrableFrame,
                      text="* Créer un livrable *", font=("Arial", 14))
        title.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack()
        self.livrableFrame.pack()
        self.confirmationFrame.pack(pady=10)

    def createLivrableButtonFrame(self):
        self.createLivrableButton = Button(self.buttonFrame, text="Créer", command=self.saveLivrable)
        self.backButton = Button(self.buttonFrame, text="Retour au menu", command=self.backToMenu)
        if self.dontcreate:
            self.createLivrableButton['state'] = DISABLED
        self.createLivrableButton.pack(side=LEFT)
        self.backButton.pack(side=RIGHT)
   
    def createLivrableFrame(self):
        fields = ["Titre", "Propriétaire","Évènement associé", "Échéancier associé", "Date Limite", "Notes"]
        row = 0
        #print(self.parent.getUserRole())
        for i in fields:

            entryLabel = Label(self.infoFrame, text=i)

            if "Titre" in i:
                entry = Entry(self.infoFrame)
                if "Titre" in self.livrableInfo:
                    entry.insert(0, self.livrableInfo["Titre"].get())
            elif "Évènement associé" in i:
                entry = self.createDropDownMenu("event")
                if self.indexEventSelect != None:
                    entry.current(self.indexEventSelect)
            elif "Échéancier associé" in i:
                entry = self.createDropDownMenu("echeancier")
                if self.indexEventSelect != None:
                    entry.current(self.indexEcheancierSelect)
                    if self.indexEcheancierSelect != None:
                        entry.current(self.indexEcheancierSelect)
                else:
                    entry.config(state='disabled')
            elif "Propriétaire" in i:                
                entry = Entry(self.infoFrame, width=50)
                entry.insert(0, self.parent.getUsername())
                entry.config(state='disabled')
            elif "Date Limite" in i:                       
                entry = DateEntry(self.infoFrame, width=12, background='darkblue',
                foreground='white', borderwidth=2, date_pattern='y-mm-dd', firstweekday='sunday')                    
                if self.indexEcheancierSelect != None:
                    echeanciers = self.parent.getEcheanciers(self.indexEventSelect+1)                    
                    if echeanciers != "Rien":
                        for echeancier in echeanciers:                              # converts list of lists to list of strings
                            if self.livrableInfo["Échéancier associé"].get() == echeancier[0]:
                                entry.set_date(echeancier[2])   
                    
                entry.config(state='disabled') 
                                
                    

            elif "Notes" in i:                
                entry = scrolledtext.ScrolledText(self.infoFrame, width=15, height=6) 
                if "Notes" in self.livrableInfo:
                    entry.insert(END, self.livrableInfo["Notes"].get("1.0",END).strip())                    
                

            entryLabel.grid(row=row, column=0, sticky=E + W)
            entry.grid(row=row, column=1, sticky=E + W)
            row += 1
            self.livrableInfo[i] = entry



    def updateLivrables(self):
        params = {}
        params["id"] = self.livrable["id"]
        params["notes"] = self.livrableInfo["Notes"].get("1.0",END).strip()        
        self.parent.updateLivrable(params)

    def createDropDownMenu(self, table):     
        n = StringVar()
        dropdownMenu = Combobox(self.infoFrame, width=27, textvariable=n)
        if table == "event":                               
            choices = self.parent.getEvents()          # returns a list of lists
        if table == "echeancier":
            idEvent = 1 if self.indexEventSelect == None else self.indexEventSelect + 1
            choices = self.livrableEcheanciersList =self.parent.getEcheanciers(idEvent)
       
        self.existingChoice = []
        if choices == "Rien":
            self.dontcreate = True
            self.existingChoice.append("Aucun échéancier")            
        else:            
            for choice in choices:                              # converts list of lists to list of strings
                self.existingChoice.append(choice[0])          # avoids curly braces from appearing in drop down menu

        dropdownMenu['values'] = self.existingChoice
        dropdownMenu.state(["readonly"])

        dropdownMenu.grid(column=1, row=15)
        if table == "event":
            dropdownMenu.current(1)                    
            dropdownMenu.bind("<<ComboboxSelected>>", self.comboEventSelection)  
        if table == "echeancier":
            dropdownMenu.current(0) 
            dropdownMenu.bind("<<ComboboxSelected>>", self.comboEcheancierSelection)
        return dropdownMenu

    def  comboEventSelection(self, event):
        self.indexEventSelect = self.livrableInfo["Évènement associé"].current()         
        self.indexEcheancierSelect = None
        self.dontcreate = True
       


        self.livrableFrame.pack_forget()
        self.addLivrableFrame()

    def comboEcheancierSelection(self, event):
        self.indexEcheancierSelect = self.livrableInfo["Échéancier associé"].current()
        if self.livrableInfo["Échéancier associé"].get() != "Aucun échéancier":
            self.dontcreate = False
        self.livrableInfo["echeancierID"] = self.livrableEcheanciersList[self.indexEcheancierSelect][1]
        self.livrableFrame.pack_forget()        
        self.addLivrableFrame()
     

        


    def clearAllFields(self):
        self.livrableInfo["Titre"].delete(0, "end")
        self.livrableInfo["État"].delete(0, "end")
        self.livrableInfo["Propriétaire"].delete(0, "end")

        if self.messageLabel:
            self.messageLabel.destroy()

    def saveLivrable(self):
        self.params = {}
   
        self.params["Titre"] = self.livrableInfo["Titre"].get()
        self.params["Owner"] = self.parent.getUserEmail()
        self.params["Echeancier"] = self.livrableInfo["echeancierID"]
        self.params["Notes"] = self.livrableInfo["Notes"].get("1.0",END).strip()  

        self.parent.saveLivrable(self.params)

    def completeLivrable(self):
        valeur = 0 if self.listeComplete == 1 else 1
        self.parent.completeLivrable(self.livrable["id"], valeur)
        self.backToMenu()

    def backToMenu(self):
        self.livrableFrame.pack_forget()
        self.createModuleFrame()

    def showMessage(self, reponseServeur):
        self.messageLabel = Label(self.confirmationFrame, text=reponseServeur)
        self.messageLabel.pack()

    def livrableDetails(self):
        selection = self.livrableList.get(self.livrableList.curselection())
        
        if selection != None:            
            for i in self.listeLivrables:
                if i[1] == selection:     
                    self.livrable["status"] = "Complété" if i[4] else "Incomplet"          
                    self.livrable["desc"] = i[1]
                    self.livrable["echeancier"] = self.parent.getEcheancier(i[2])                    
                    self.livrable["responsable"] = self.parent.getUser(i[3])
                    self.livrable["id"] = i[0]
                    self.livrable["notes"] = i[5]
                    

            self.gestionFrame.destroy()
            self.createDetailsFrame()
            self.createDetailsButtonFrame()
        else:
            print("Veuillez sélectionner un livrable")


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
        print(sys.argv)

    def getUsername(self):
        return self.modele.username

    def getUserRole(self):
        return self.modele.userRole

    def getUserEmail(self):
        return self.modele.courriel

    def saveLivrable(self, newlivrable):
        reponseServeur = self.connexion.saveLivrable(newlivrable)
        self.vue.showMessage(reponseServeur)

    def getLivrables(self, complete):
        return self.connexion.getLivrables(self.modele.courriel, complete)

    def updatelivrable(self, updateData):
        reponseServeur = self.connexion.updateLivrable(updateData)
        self.vue.showMessage(reponseServeur)

    def getEcheancier(self, id):
        return self.connexion.populate("echeancier", id)

    def getUser(self, id):
        return self.connexion.populate("personnels", id)

    def appelserveur(self, route, params):
        return self.connexion.appelserveur(route, params)

    def completeLivrable(self, id, valeur):
        self.connexion.completeLivrable(id, valeur)

    def updateLivrable(self, params):
        self.connexion.updateLivrable(params)
    
    def getEvents(self):
        return self.connexion.getEvent()

    def getEcheanciers(self, idEvent):
        return self.connexion.getEcheanciers(idEvent)

  


if __name__ == '__main__':
    c = Controleur()
