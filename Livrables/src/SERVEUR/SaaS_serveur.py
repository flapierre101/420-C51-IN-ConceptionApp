#import flask
from tkinter.constants import INSERT
from flask import Flask, request, json
from werkzeug.wrappers import Response
import os
# pour retrouver le dossier courant d'execution
import sys

import sqlite3

app = Flask(__name__)

app.secret_key = "qwerasdf1234"
MAX_CLIENT_F1 = 5
MAX_CLIENT_F2 = 500
MAX_CLIENT_F3 = 1500

class Dbclient():
    def __init__(self):
        nomdb = os.getcwd()+"/SaaS_DB/"+"Production_CDJ_client.sqlite"
        self.conn = sqlite3.connect(nomdb)
        self.curs = self.conn.cursor()

    def getEvent(self):
        sqlnom = (
            "select nom, date_debut, date_fin, budget, desc, id from 'evenement'")
        self.curs.execute(sqlnom)
        info = self.curs.fetchall()
        return info

    def trouverclients(self):
        sqlnom = ("select compagnie, nom, courriel from 'client'")
        self.curs.execute(sqlnom)
        info = self.curs.fetchall()
        return info

    def fermerdb(self):
        self.conn.close()

    def updateEvent(self, updateData):
        sqlRequest = ('''
            Update Evenement
                Set
                    nom = ?,
                    date_debut = ?,
                    date_fin = ?,
                    budget = ?,
                    desc = ?
            Where id = ?''')

        try:
            self.curs.execute(sqlRequest, updateData)
            self.conn.commit()
            return "Evenement mis a jour !"
        except sqlite3.Error as er:
            print(er)
            return "Echec de la mise a jour !"

    def getOneEvent(self, event):
        sqlRequest = (
            "select nom, date_debut, date_fin, desc, id from 'evenement' where nom = ?")
        param = []
        param.append(event)
        self.curs.execute(sqlRequest, param)
        return self.curs.fetchall()

    def newEvent(self, nom, date_debut, date_fin, budget, desc):
        sqlRequest = "INSERT INTO 'evenement'(nom, date_debut, date_fin, budget, desc) VALUES (?,?,?,?,?)"
        param = [nom, date_debut, date_fin, budget, desc]
        try:
            self.curs.execute(sqlRequest, param)
            self.conn.commit()
            return self.curs.fetchall()
        except sqlite3.Error as er:
            print(er)

    def deleteEvent(self, eventID):
        sqlRequest = "DELETE FROM 'evenement' where id = ?"
        param = [eventID]
        try:
            self.curs.execute(sqlRequest, param)
            self.conn.commit()

        except sqlite3.Error as er:
            print(er)

    def getEventEcheancier(self):
        pass

    def newEcheancier(self):
        pass

    def getFournisseurList(self):
        pass

    def updateLivrable(self, id, notes):
        sqlRequest = ('''
            Update livrables
                Set
                    notes =:notes
            Where id =:id''')
        try:
            self.curs.execute(sqlRequest, {'id': id, 'notes':notes})
            self.conn.commit()
            return "Evenement mis a jour !"
        except sqlite3.Error as er:
            print(er)
            return "Echec de la mise a jour !"

    def saveLivrable(self, titre, courriel, echeancierID, notes):
        sqlnom = ( "select id from 'personnels' where courriel=:courriel")
        self.curs.execute(sqlnom, {'courriel': courriel})
        usager = self.curs.fetchall()
        if usager:
            params = [titre, echeancierID, usager[0][0], notes]
            sqlRequest = ("INSERT INTO 'livrables'(desc, echeancier, responsable, notes) VALUES (?,?,?,?)")
            try:
                self.curs.execute(sqlRequest, params)
                self.conn.commit()
                return "Livrable ajouté !"
            except sqlite3.Error as er:
                print(er)
        return "Echec de la mise a jour !"

    def saveEcheancier(self, titre, dueDate, eventID, dateRappel, descrappel):

        params = [titre, dueDate, eventID, dateRappel, descrappel]
        sqlRequest = ("INSERT INTO 'echeancier'(desc, duedate, evenement, daterappel, descrappel) VALUES (?,?,?,?,?)")
        try:
            self.curs.execute(sqlRequest, params)
            self.conn.commit()
            return "Echeancier ajouté !"
        except sqlite3.Error as er:
            print(er)
        return "Echec de la mise a jour !"

    def completeLivrable(self, id, valeur):
        sqlRequest = ('''
            Update livrables
                Set
                    complete =:valeur
            Where id=:id''')
        try:
            self.curs.execute(sqlRequest, {'id': id, 'valeur':valeur})
            self.conn.commit()
            return "Evenement mis a jour !"
        except sqlite3.Error as er:
            print(er)
            return "Echec de la mise a jour !"

    def populate(self, table, id):
        sqlnom = ( "select * from " + table + " where id=:id")
        self.curs.execute(sqlnom, {'id': id, 'table': table})
        rep = self.curs.fetchall()
        if not rep:
            rep = "Erreur"
        else:
            rep = rep[0]

        return rep

    def getLivrablesUser(self, courriel, complete):
        sqlnom = ( "select * from 'personnels' where courriel=:courriel")
        self.curs.execute(sqlnom, {'courriel': courriel})
        usager = self.curs.fetchall()
        if usager:
            sqlnom = ("select * from 'livrables' where responsable=:qui and complete=:complete")
            self.curs.execute(sqlnom, {'qui': usager[0][0], 'complete':complete})
            livrables = self.curs.fetchall()
            return livrables


        return "Rien"

    def getEcheanciers(self, event):
        sqlnom = ( "select desc, id, duedate from 'echeancier' where evenement=:event")
        self.curs.execute(sqlnom, {'event': event})
        echeanciers = self.curs.fetchall()
        if echeanciers:
            return echeanciers

        return "Rien"

    ### Module Gestion Client

    def getClients(self):
        sqlnom=("select idclient, nom, courriel, tel, compagnie, adresse, rue, ville from 'client'")
        self.curs.execute(sqlnom)
        info=self.curs.fetchall()
        return info

    def getOneClient(self, client):
        pass

    def saveClient(self, param):
        # sqlRequest = "INSERT INTO 'evenement'(nom, date_debut, date_fin, budget, desc) VALUES (?,?,?,?,?)"
        sqlRequest = "INSERT INTO 'client' (nom, courriel, tel, compagnie, adresse, rue, ville) VALUES (?,?,?,?,?,?,?)"
        try:
            self.curs.execute(sqlRequest, param)
            self.conn.commit()
            return self.curs.fetchall()
        except sqlite3.Error as er:
            print(er)
            return er


    def deleteClient(self, clientId):
        sqlRequest = "DELETE FROM 'client' where idclient = ?"
        param = [clientId]
        try:
            self.curs.execute(sqlRequest, param)
            self.conn.commit()

        except sqlite3.Error as er:
            print(er)

    def updateClient(self, updatedData):
        sqlRequest = '''
        UPDATE client
            SET nom = ?,
                courriel = ?,
                tel = ?,
                compagnie = ?,
                adresse = ?,
                rue = ?,
                ville = ?
            WHERE idclient = ?
       '''
        try:
           self.curs.execute(sqlRequest, updatedData)
           self.conn.commit()
           return "Success"

        except sqlite3.Error as er:
            print(er)


class Dbman():
    def __init__(self):
        nomdb = os.getcwd()+"/SaaS_DB/"+"Production_CDJ_corpo.sqlite"
        self.conn = sqlite3.connect(nomdb)
        #self.conn = sqlite3.connect("Production_CDJ_corpo.sqlite")
        self.curs = self.conn.cursor()

    def identifierusager(self, nom, mdp):
        sqlnom = (
            "select * from 'utilisateurs' where courriel=:qui and password=:secret")
        self.curs.execute(sqlnom, {'qui': nom, 'secret': mdp})
        usager = self.curs.fetchall()

        if usager:
            sqlnom = ("select * from 'clients' where id=:qui")
            self.curs.execute(sqlnom, {'qui': usager[0][1]})
            compagnie = self.curs.fetchall()
            return [usager, compagnie]
        return "inconnu"

    def getRoles(self):
        sqlRequest = ("select distinct role from 'utilisateurs'")
        self.curs.execute(sqlRequest)
        info = self.curs.fetchall()
        return info

    def getPermissions(self):
        sqlRequest = ("select distinct droit from 'utilisateurs'")
        self.curs.execute(sqlRequest)
        info = self.curs.fetchall()
        return info

    def getCompanyID(self,company):
        sqlRequest = ("select id from clients where nom = ?")
        param = [company]
        self.curs.execute(sqlRequest,param)
        id = self.curs.fetchall()
        return id

    def newUser(self, compagnie,password,nom,prenom,courriel,role,droit):
        sqlRequest = ("INSERT INTO 'utilisateurs'(compagnie, password, nom, prenom, courriel, role, droit) VALUES (?,?,?,?,?,?,?)")
        try:
            param = [compagnie,password,nom,prenom,courriel,role,droit]
            self.curs.execute(sqlRequest, param)
            self.conn.commit()
            return self.curs.fetchall()
        except sqlite3.Error as er:
            print(er)


    def trouvermembres(self):
        sqlnom = (
            "select Prenom || ' ' || Nom as nomcomplet, courriel,role, droit from 'utilisateurs'")
        self.curs.execute(sqlnom)
        info = self.curs.fetchall()
        return info

    def fermerdb(self):
        self.conn.close()

    def updateForfaitClient(self, compagnie, forfait):
        sqlRequest = ("update clients set forfait = ? where id = ?")
        listData = [forfait, compagnie]
        try:
            self.curs.execute(sqlRequest, listData)
            self.conn.commit()
            return self.curs.fetchall()
        except sqlite3.Error as er:
            print(er)

def demanderclients():
    db = Dbclient()
    clients = db.trouverclients()
    db.fermerdb()
    return clients


mesfonctions = {"demanderclients": demanderclients}


@app.route('/')
def index():
    return 'Hello world du serveur ' + os.getcwd()


@app.route('/trouvermodules', methods=["GET", "POST"])
def trouvermodules():
    listefichiers = []
    monhome = os.path.dirname(os.path.realpath(sys.argv[0]))+"/SaaS_modules"
    # monhome=os.getcwd()+"/SaaS_modules"
    listefichiers = os.listdir(monhome)
    return Response(json.dumps(listefichiers), mimetype='application/json')


@app.route('/telechargermodule', methods=["GET", "POST"])
def telechargermodule():
    if request.method == "POST":
        fichier = request.form["fichier"]
        monhome = os.path.dirname(
            os.path.realpath(sys.argv[0]))+"/SaaS_modules"
        bonfichier = open(monhome+"/"+fichier)
        lemodule = bonfichier.read()
        bonfichier.close()
        return Response(json.dumps(lemodule), mimetype='application/json')
        # return repr(usager)
    else:
        return repr("pas ok")


@app.route('/identifierusager', methods=["GET", "POST"])
def identifierusager():
    if request.method == "POST":
        nom = request.form["nom"]
        mdp = request.form["mdp"]
        db = Dbman()
        usager = db.identifierusager(nom, mdp)

        db.fermerdb()
        return Response(json.dumps(usager), mimetype='application/json')
        # return repr(usager)
    else:
        return repr("pas ok")


@app.route('/getEvent', methods=["GET", "POST"])
def getEvent():
    if request.method == "POST":
        db = Dbclient()
        events = db.getEvent()
        db.fermerdb()
        return Response(json.dumps(events), mimetype='application/json')
    else:
        return repr("pas ok")


@app.route('/getRoles', methods=["GET", "POST"])
def getRoles():
    if request.method == "POST":
        db = Dbman()
        roles = db.getRoles()
        db.fermerdb()
        return Response(json.dumps(roles), mimetype='application/json')
    else:
        return repr("Erreur")

@app.route('/getPermissions', methods=["GET", "POST"])
def getPermissions():
    if request.method == "POST":
        db = Dbman()
        permissions = db.getPermissions()
        db.fermerdb()
        return Response(json.dumps(permissions), mimetype='application/json')
    else:
        return repr("Erreur")

@app.route('/getCompanyID', methods=["GET", "POST"])
def getCompanyID():
    if request.method == "POST":
        db = Dbman()
        compagnie = request.form["compagnie"]
        id = db.getCompanyID(compagnie)
        db.fermerdb()
        return Response(json.dumps(id), mimetype='application/json')
    else:
        return repr("Erreur")


@app.route('/trouvermembres', methods=["GET", "POST"])
def trouvermembres():
    if request.method == "POST":
        db = Dbman()
        membres = db.trouvermembres()

        db.fermerdb()
        return Response(json.dumps(membres), mimetype='application/json')
        # return repr(usager)
    else:
        return repr("pas ok")


@app.route('/requeteserveur', methods=["GET", "POST"])
def requeteserveur():
    if request.method == "POST":
        nomfonction = request.form["fonction"]
        rep = mesfonctions[nomfonction]()
        return Response(json.dumps(rep), mimetype='application/json')
        # return repr(usager)
    else:
        return repr("pas ok")


@app.route('/getOneEvent', methods=["GET", "POST"])
def getOneEvent():
    if request.method == "POST":
        nomEvent = request.form["nom"]
        db = Dbclient()
        eventList = db.getOneEvent(nomEvent)
        db.fermerdb()
        return Response(json.dumps(eventList), mimetype='application/json')

    else:
        return repr("Error")


@app.route('/deleteEvent', methods=["GET", "POST"])
def deleteEvent():
    message = ""
    if request.method == "POST":
        id = request.form["id"]
        db = Dbclient()
        db.deleteEvent(id)
        db.fermerdb()
        message = "Success"
    else:
        message = "Error"

    return Response(json.dumps(message), mimetype='application/json')


@app.route('/updateEvent', methods=["GET", "POST"])
def updateEvent():
    updateData = []
    if request.method == "POST":
        db = Dbclient()
        updateData.append(request.form["nom"])
        updateData.append(request.form["date_debut"])
        updateData.append(request.form["date_fin"])
        updateData.append(request.form["budget"])
        updateData.append(request.form["desc"])
        updateData.append(request.form["id"])
        return db.updateEvent(updateData)


@app.route('/updateForfait', methods=["GET", "POST"])
def updateForfait():
    if request.method == "POST":
        forfait = request.form["forfait"]
        compagnieID = request.form["compagnieID"]
        db = Dbman()
        db.updateForfaitClient(compagnieID, forfait)
        db.fermerdb()
        # return Response(json.dumps(eventList), mimetype='application/json')
        return Response(json.dumps("ok"), mimetype='application/json')

    else:
        return repr("Error")



@app.route('/newEvent', methods=["GET", "POST"])
def newEvent():
    if request.method == "POST":
        nom = request.form["nom"]
        date_debut = request.form["date_debut"]
        date_fin = request.form["date_fin"]
        budget = request.form["budget"]
        desc = request.form["desc"]
        db = Dbclient()
        db.newEvent(nom, date_debut, date_fin, budget, desc)
        return "test"

@app.route('/newUser', methods=["GET", "POST"])
def newUser():
    message = ""
    if request.method == "POST":

        try:
            compagnie = request.form["compagnie"]
            password = request.form["defaultPassword"]
            nom = request.form["nom"]
            prenom = request.form["prenom"]
            courriel = request.form["courriel"]
            role = request.form["role"]
            droit = request.form["droit"]
            db = Dbman()
            rep = db.newUser(compagnie,password,nom,prenom,courriel,role,droit)
            message = "Success"
        except:
            message = "Erreur"
        return Response(json.dumps(message), mimetype='application/json')


@app.route('/newLivrable', methods=["GET", "POST"])
def newLivrable():
    if request.method == "POST":

        titre = request.form["Titre"]
        courriel = request.form["Owner"]
        echeancierID = request.form["Echeancier"]
        notes = request.form["Notes"]

        db = Dbclient()
        resultat = db.saveLivrable(titre, courriel, echeancierID, notes)
        db.fermerdb()
        return Response(json.dumps(resultat), mimetype='application/json')
    else:
        return repr("Error")

@app.route('/saveEcheancier', methods=["GET", "POST"])
def saveEcheancier():
    if request.method == "POST":


        eventID = request.form["eventID"]
        dueDate = request.form["dueDate"]
        dateRappel = request.form["dateRappel"]
        descrappel = request.form["descrappel"]
        titre = request.form["titre"]

        db = Dbclient()
        resultat = db.saveEcheancier(titre, dueDate, eventID, dateRappel, descrappel)
        db.fermerdb()
        return Response(json.dumps(resultat), mimetype='application/json')
    else:
        return repr("Error")

@app.route('/deleteLivrable', methods=["GET", "POST"])
def deleteLivrable():
    if request.method == "POST":
        pass
    else:
        return repr("Error")


@app.route('/completeLivrable', methods=["GET", "POST"])
def completeLivrable():
    if request.method == "POST":
        valeur = request.form["valeur"]
        id = request.form["id"]
        db = Dbclient()
        resultat = db.completeLivrable(id, valeur)
        db.fermerdb()
        return Response(json.dumps(resultat), mimetype='application/json')
    else:
        return repr("pas ok")


@app.route('/getLivrables', methods=["GET", "POST"])
def getLivrable():
    if request.method == "POST":
        courriel = request.form["courriel"]
        complete = request.form["complete"]
        db = Dbclient()
        livrables = db.getLivrablesUser(courriel, complete)
        db.fermerdb()
        return Response(json.dumps(livrables), mimetype='application/json')
    else:
        return repr("pas ok")

@app.route('/getEcheanciers', methods=["GET", "POST"])
def getEcheanciers():
    if request.method == "POST":
        event = request.form["event"]

        db = Dbclient()
        echanciers = db.getEcheanciers(event)
        db.fermerdb()
        return Response(json.dumps(echanciers), mimetype='application/json')
    else:
        return repr("pas ok")

@app.route('/updateLivrable', methods=["GET", "POST"])
def updateLivrable():
    if request.method == "POST":
        id = request.form["id"]
        notes = request.form["notes"]
        db = Dbclient()
        livrables = db.updateLivrable(id, notes)
        db.fermerdb()
        return Response(json.dumps(livrables), mimetype='application/json')
    else:
        return repr("pas ok")

# Sers à populer les données propres à un foreign key dans une table.
@app.route('/populate', methods=["GET", "POST"])
def populate():
    if request.method == "POST":
        table = request.form["table"]
        id = request.form["id"]
        db = Dbclient()
        resultat = db.populate(table, id)
        db.fermerdb()
        return Response(json.dumps(resultat), mimetype='application/json')
    else:
        return repr("pas ok")


### ROUTES CLIENTS
@app.route('/getClients', methods=["GET", "POST"])
def getClients():
    db = Dbclient()
    data = db.getClients()
    db.fermerdb()
    return Response(json.dumps(data), mimetype='application/json')

@app.route('/getMaxClient', methods=["GET", "POST"])
def maxClient():
    infoClient = request.form["coData"]
    maxclientT = globals()["MAX_CLIENT_F" + infoClient]
    return str(maxclientT)

@app.route('/save_client', methods=["GET", "POST"])
def save_client():
    param = []
    if request.method == "POST":
        if request.form["nom"] != '':
            param.append(request.form["nom"])
            param.append(request.form["courriel"])
            param.append(request.form["telephone"])
            param.append(request.form["compagnie"])
            param.append(request.form["adresse"])
            param.append(request.form["rue"])
            param.append(request.form["ville"])
            try:
                db = Dbclient()
                rep = db.saveClient(param)
                return str(rep)
            except:
                rep = "Erreur dans la route"
                return rep
        else:
            return "Pas de ID"

@app.route('/deleteClient', methods=["GET", "POST"])
def deleteClient():
    if request.method == "POST":
        id = request.form["id"]
        db = Dbclient()
        db.deleteClient(id)
        db.fermerdb()
        message = "Success"
    else:
        message = "Error"
    return Response(json.dumps(message), mimetype='application/json')

@app.route('/updateClient', methods=["GET", "POST"])
def updateClient():
    param = []
    if request.method == "POST":
        if request.form["idclient"] != '':
            param.append(request.form["nom"])
            param.append(request.form["courriel"])
            param.append(request.form["telephone"])
            param.append(request.form["compagnie"])
            param.append(request.form["adresse"])
            param.append(request.form["rue"])
            param.append(request.form["ville"])
            param.append(request.form["idclient"])
            try:
                db = Dbclient()
                rep = db.updateClient(param)

                return "Success" + str(rep)
            except:
                rep = "Erreur dans la route"
                return rep
        else:
            return "Erreur"


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True, host='127.0.0.1', port=5000)
