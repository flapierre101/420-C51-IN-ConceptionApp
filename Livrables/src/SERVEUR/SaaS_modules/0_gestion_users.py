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
        self.courriel = None
        self.userParam = {}
        self.modifyUser = False
        self.userToModify = []
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

        self.userList.bind('<ButtonRelease-1>', self.getSelection)

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
        self.createModifyButton = Button(self.buttonFrame, text="Modifier un employé",command=self.createModifyUser)
        # self.eventPersonnelButton = Button(self.buttonFrame, text="Employés de ")

        self.createAddButton.pack(fill=Y)
        self.createModifyButton.pack(fill=Y)

    def createRolesDropDownMenu(self):
        n = StringVar()
        self.rolesMenu = Combobox(self.infoFrame, width=27,
                                    textvariable=n)

        roles = self.parent.getExistingRoles()          # returns a list of lists
        self.existingRoles = []

        for role in roles:                              # converts list of lists to list of strings
            self.existingRoles.append(role[0])          # avoids curly braces from appearing in drop down menu

        self.rolesMenu['values'] = self.existingRoles
        self.rolesMenu.state(["readonly"])

        self.rolesMenu.grid(column=1, row=15)
        self.rolesMenu.current(0)
        return self.rolesMenu

    def createPermissionsDropDownMenu(self):
        n = StringVar()
        self.permissionsMenu = Combobox(self.infoFrame, width=27,
                                    textvariable=n)

        self.permissions = self.parent.getExistingPermissions()
        self.droits = []

        for droit in self.permissions:
            self.droits.append(droit[0])

        self.permissionsMenu['values'] = self.droits
        self.permissionsMenu.state(["readonly"])

        self.permissionsMenu.grid(column=1, row=15)
        self.permissionsMenu.current(0)
        return self.permissionsMenu

    def createNewUser(self):
        self.mainFrame.destroy()
        self.addUserFrame()

    def createModifyUser(self):
        self.mainFrame.destroy()
        self.modifyUser = True
        self.addUserFrame()

    def getSelection(self, event):
        curItem = self.userList.focus()
        values = ()
        values = self.userList.item(curItem, 'values')
        item = values[2]
        self.courriel = item
        self.getUserInfo(item)                 # courriel du user à modifier



    def getUserInfo(self, email):

        self.userToModify = self.parent.getUserInfo(email)
        self.dateEmbauche = self.parent.getEmploymentDate(email)                # returns list of lists
        self.date = None

        for date in self.dateEmbauche:
            self.date = date[0]                                                 # to extract string from list
        self.userDetails()

    def userDetails(self):
        for i in self.userToModify:

            self.user["id"] = i[0]
            self.user["compagnie"] = self.parent.company
            self.user["nom"] = i[3]
            self.user["prenom"] = i[4]
            self.user["courriel"] = i[5]
            self.user["role"] = i[6]
            self.user["droit"] = i[7]
            self.user["dateEmbauche"] = self.date

    def addUserFrame(self):
        self.root.geometry("325x325")
        self.userFrame = Frame(self.root)
        self.infoFrame = Frame(self.userFrame)
        self.buttonFrame = Frame(self.userFrame)
        self.confirmationFrame = Frame(self.userFrame)

        titleText = ""
        if(self.modifyUser):
            self.addUserInfo()
            titleText = "* Modifier un utilisateur *"
        else:
            self.createInfoFrame()
            titleText = "* Créer un utilisateur *"

        self.createUserButtonFrame()


        title = Label(self.userFrame,
                      text=titleText, font=("Arial", 14))
        title.pack()
        self.infoFrame.pack()
        self.buttonFrame.pack()
        self.confirmationFrame.pack(pady=10)
        self.userFrame.pack()


    def createInfoFrame(self):
        fields = ["Compagnie", "Nom", "Prénom", "Rôle", "Droits", "Courriel", "Date d'embauche"]
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
                entry = self.createRolesDropDownMenu()
            elif "Droits" in i:
                entry = self.createPermissionsDropDownMenu()

            else:
                entry = Entry(self.infoFrame)

            entryLabel.grid(row=row, column=0, sticky=E + W)
            entry.grid(row=row, column=1, sticky=E + W)
            row += 1
            self.userInfo[i] = entry

    def addUserInfo(self):
        fields = ["Nom", "Prénom", "Rôle", "Droits", "Courriel", "Date d'embauche"]
        row = 0

        for i in fields:
            entryLabel = Label(self.infoFrame, text=i)

            if "Date" in i:
                entry = DateEntry(self.infoFrame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, date_pattern='y-mm-dd', firstweekday='sunday')
                entry.set_date(self.user["dateEmbauche"])
            elif "Compagnie" in i:
                entry = Entry(self.infoFrame)
                company = self.parent.getCompany()
                entry.insert(0,company)
                entry.configure(state="disabled")
            elif "Rôle" in i:
                entry = self.createRolesDropDownMenu()
                for j in range(len(self.existingRoles)):
                    if self.existingRoles[j] == self.user["role"]:
                        entry.current(j)
            elif "Droits" in i:
                entry = self.createPermissionsDropDownMenu()
                for j in range(len(self.droits)):
                    if self.droits[j] == self.user["droit"]:
                        entry.current(j)
            elif "Prénom" == i:
                entry = Entry(self.infoFrame)
                entry.insert(0,self.user["prenom"])
            elif "Nom" == i:
                entry = Entry(self.infoFrame)
                entry.insert(0,self.user["nom"])
            elif "Courriel" in i:
                entry = Entry(self.infoFrame)
                entry.insert(0,self.user["courriel"])

            entryLabel.grid(row=row, column=0, sticky=E + W)
            entry.grid(row=row, column=1, sticky=E + W)
            row += 1
            self.userInfo[i] = entry



    def getUserEntryData(self):
        self.userParam = {}

        self.userParam["compagnie"] = sys.argv[4]
        self.userParam["defaultPassword"] = "AAAaaa111"
        self.userParam["nom"] = self.userInfo["Nom"].get()
        self.userParam["prenom"] = self.userInfo["Prénom"].get()
        self.userParam["courriel"] = self.userInfo["Courriel"].get()
        self.userParam["role"] = self.userInfo["Rôle"].get()
        self.userParam["droit"] = self.userInfo["Droits"].get()

        if not self.modifyUser:
            repUser = self.parent.saveUser(self.userParam)

            if repUser == "Success":
                repEmployee = self.getEmployeeEntryData()

                if repEmployee == "Success":
                    self.showMessage("Nouvel utilisateur créé avec succès")
        else:
            self.userParam["ancienCourriel"] = self.courriel
            repUser = self.parent.updateUser(self.userParam)

            if repUser == "Success":
                repEmployee = self.getEmployeeEntryData()

                if repEmployee == "Success":
                    self.showMessage("Utilisateur modifié avec succès")

    def getEmployeeEntryData(self):
        param = {}

        param["compagnie"] = self.parent.getCompany()
        param["nom"] = self.userInfo["Nom"].get()
        param["prenom"] = self.userInfo["Prénom"].get()
        param["courriel"] = self.userInfo["Courriel"].get()
        param["role"] = self.userInfo["Rôle"].get()
        param["dateEmbauche"] = self.userInfo["Date d'embauche"].get_date()

        if not self.modifyUser:
            return self.parent.saveEmployee(param)
        else:
            param["ancienCourriel"] = self.courriel
            return self.parent.updateEmployee(param)


    def createUserButtonFrame(self):

        if self.modifyUser:
            self.createModifyUserButton = Button(self.buttonFrame, text="Modifier", command=self.getUserEntryData)
            self.createModifyUserButton.pack(side=LEFT)
        else:
            self.createUserButton = Button(self.buttonFrame, text="Créer", command=self.getUserEntryData)
            self.createUserButton.pack(side=LEFT)

        self.backButton = Button(self.buttonFrame, text="Retour au menu", command=self.backToMenu)
        self.clearButton = Button(self.buttonFrame, text="Effacer", command=self.clearAllFields)

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
        self.userInfo["Droits"].delete(0, "end")
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
        self.getCompany()
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def getExistingRoles(self):
        return self.connexion.getRoles()

    def getExistingPermissions(self):
        return self.connexion.getPermissions()

    def getUserInfo(self, email):
        return self.connexion.getUser(email)

    def getUsername(self):
        self.username = sys.argv[2]
        return self.username

    def getEmploymentDate(self,email):
        return self.connexion.getDate(email)

    def getUserPermissions(self):
        self.userPermissions = sys.argv[1]
        return self.userPermissions

    def getCompany(self):
        companyInfo = []
        self.companyInfo = json.loads(sys.argv[4])
        self.company = self.companyInfo["nom"]
        self.companyID = self.companyInfo["id"]
        return self.company

    def getCompanyID(self, compagnie):
        id = self.connexion.getCompanyID(compagnie)
        id = id[0][0]
        return int(id)

    def getUsers(self):
        return self.connexion.trouvermembres()

    def saveUser(self, newUser):
        return self.connexion.saveUser(newUser)

    def updateUser(self, user):
        return self.connexion.updateUser(user)

    def saveEmployee(self, newEmployee):
        return self.connexion.saveEmployee(newEmployee)

    def updateEmployee(self, employee):
        return self.connexion.updateEmployee(employee)

if __name__ == '__main__':
    c = Controleur()
