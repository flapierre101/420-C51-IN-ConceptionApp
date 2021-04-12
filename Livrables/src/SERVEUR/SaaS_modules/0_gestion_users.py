from tkinter import *
from tkinter.ttk import *
# à copier dans chaque nouveau module pour avoir la classe connexion
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../connexion.py
from connexion import *


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.welcomeLabel = Label(self.root, text="Bienvenue " + self.parent.getUsername(), font=("Arial", 14)).pack()
        self.title = Label(self.root, text="*** Gestion d'utilisateurs ***", font=("Arial", 16)).pack()
        self.createModuleFrame()

    def createModuleFrame(self):
        self.mainFrame = Frame(self.root)
        self.listeEmployes = self.parent.getUsers()
        self.root.geometry("600x475")
        self.listFrame = Frame(self.mainFrame)
        self.buttonFrame = Frame(self.mainFrame)
        self.userList = Treeview(self.listFrame)
        self.userList["columns"]=("1","2","3")
        self.userList["show"] = 'headings'
        self.userList["selectmode"] = 'browse'
        self.userList.column("1",width=150,anchor='w')
        self.userList.column("2",width=125,anchor='c')
        self.userList.column("3",width=125,anchor='c')
        self.userList.heading("1",text="Nom")
        self.userList.heading("2",text="Titre")
        self.userList.heading("3",text="Courriel")

        print(self.listeEmployes)

        row = 1

        for i in self.listeEmployes:
            self.userList.insert("",'end',values=(i[0],i[2],i[1]))
            row += 1

        listLabel = Label(self.listFrame, text="Liste des utilisateurs")
        listLabel.pack()
        self.userList.pack()

        self.listFrame.pack(side=LEFT)

        self.createButtonFrame()
        self.buttonFrame.pack(padx=20)
        self.mainFrame.pack()

    def createButtonFrame(self):
        self.createAddButton = Button(self.buttonFrame, text="Ajouter un employé",command=self.getEntryData)
        self.createModifyButton = Button(self.buttonFrame, text="Modifier un employé")
        # self.eventPersonnelButton = Button(self.buttonFrame, text="Employés de ")

        self.createAddButton.pack(fill=Y)
        self.createModifyButton.pack(fill=Y)

    def getEntryData(self):
        param = {}
        item = self.userList.selection()

        for i in item:
            print(self.userList.item(i, "values"))

        return param



class Modele():
    def __init__(self, parent):
        self.parent = parent


class Controleur():
    def __init__(self):
        self.nomUser = sys.argv[1]
        self.modele = Modele(self)
        self.connexion = Connexion()
        self.urlserveur = self.connexion.urlserveur
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def getUsername(self):
        self.username = sys.argv[2]
        return self.username

    def getUserRole(self):
        self.userRole = sys.argv[1]
        return self.userRole

    def getUsers(self):
        return self.connexion.trouvermembres()

if __name__ == '__main__':
    c = Controleur()
