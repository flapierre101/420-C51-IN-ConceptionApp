from tkinter import *
from tkinter.ttk import *
from tkcalendar import *
import datetime
import json

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
        self.userInfo = {}
        self.root.title("Production CDJ - Utilisateurs")
        self.user = {}
        self.userParam = {}
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
        self.createAddButton = Button(self.buttonFrame, text="Ajouter un employé",command=self.createNewUser)
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

    def createDropDownMenu(self):
        company = self.parent.getCompany()
        #self.roles = self.parent.getExistingRoles(company)
        # TODO get correct sql request/table

        n = StringVar()
        rolesMenu = Combobox(self.infoFrame, width=27,
                                    textvariable=n)

        # Adding combobox drop down list
        rolesMenu['values'] = ('Admin','RH','Employé')

        rolesMenu.grid(column=1, row=15)
        rolesMenu.current(2)
        return rolesMenu

    def createNewUser(self):
        self.mainFrame.destroy()
        self.addUserFrame()

    def addUserFrame(self):
        self.root.geometry("325x325")
        self.userFrame = Frame(self.root)
        self.infoFrame = Frame(self.userFrame)
        self.buttonFrame = Frame(self.userFrame)
        self.confirmationFrame = Frame(self.userFrame)

        self.createInfoFrame()
        self.createUserButtonFrame()

        title = Label(self.userFrame,
                      text="* Créer un utilisateur *", font=("Arial", 14))
        title.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack()
        self.userFrame.pack()
        self.confirmationFrame.pack(pady=10)

    def createInfoFrame(self):
        fields = ["Compagnie", "Nom", "Prénom", "Rôle", "Courriel", "Date d'embauche"]
        row = 0

        for i in fields:

            entryLabel = Label(self.infoFrame, text=i)

            if "Date" in i:
                entry = DateEntry(self.infoFrame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, date_pattern='y-mm-dd', firstweekday='sunday')
            elif "Compagnie" in i:
                entry = Entry(self.infoFrame)
                company = self.parent.getCompany()
                entry.insert(0,company)
                entry.configure(state="disabled")
            elif "Rôle" in i:
                entry = self.createDropDownMenu()
            else:
                entry = Entry(self.infoFrame)

            entryLabel.grid(row=row, column=0, sticky=E + W)
            entry.grid(row=row, column=1, sticky=E + W)
            row += 1
            self.userInfo[i] = entry


    def createUserButtonFrame(self):
        self.createUserButton = Button(self.buttonFrame, text="Créer", command=self.parent.saveUser)
        self.backButton = Button(self.buttonFrame, text="Retour au menu", command=self.backToMenu)
        self.clearButton = Button(self.buttonFrame, text="Effacer", command=self.clearAllFields)
        self.createUserButton.pack(side=LEFT)
        self.clearButton.pack(side=LEFT)
        self.backButton.pack(side=RIGHT)

    def backToMenu(self):
        self.userFrame.pack_forget()
        self.createModuleFrame()

    def showMessage(self, reponseServeur):

        self.messageLabel = Label(self.confirmationFrame, text=reponseServeur)
        self.messageLabel.pack()

    def clearAllFields(self):
        self.userInfo["Nom"].delete(0, "end")
        self.userInfo["Prénom"].delete(0, "end")
        self.userInfo["Rôle"].delete(0, "end")
        self.userInfo["Courriel"].delete(0, "end")
        self.userInfo["Date d'embauche"].set_date(datetime.date.today())

        if self.messageLabel:
            self.messageLabel.destroy()





class Modele():
    def __init__(self, parent):
        self.parent = parent


class Controleur():
    def __init__(self):
        self.nomUser = sys.argv[1]
        self.modele = Modele(self)
        self.connexion = Connexion()
        self.urlserveur = self.connexion.urlserveur
        self.company = None
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def getExistingRoles(self,company):
        #return self.connexion.getRoles(company)
        pass

    def getUsername(self):
        self.username = sys.argv[2]
        return self.username

    def getUserRole(self):
        self.userRole = sys.argv[1]
        return self.userRole

    def getCompany(self):
        companyInfo = []
        self.companyInfo = json.loads(sys.argv[4])
        self.company = self.companyInfo["nom"]
        return self.company

    def getUsers(self):
        return self.connexion.trouvermembres()

    def saveUser(self, newUser):
        #reponseServeur = self.connexion.saveEvent(newUser)
        #self.vue.showMessage(reponseServeur)
        pass

if __name__ == '__main__':
    c = Controleur()
