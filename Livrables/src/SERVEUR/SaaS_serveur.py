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
        print("dans updateDAta ", updateData)
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

    def newFournisseur(self):
        pass

    def getEcheancierLivrable(self):
        pass


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

    # def updateDB(self, tableName, col, val, id):
    #     sqlRequest = (
    #         "Update"+tableName+
    #         "Set" + col + "=" + val +
    #         "Where id =" + id)
    #     try:
    #         self.curs.execute(sqlRequest)
    #         self.conn.commit()
    #     except sqlite3.Error as er:
    #         print(er)


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
        eventDeleted = db.deleteEvent(id)
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
        print("params reçus: ", forfait, compagnieID)
        db = Dbman()
        db.updateForfaitClient(compagnieID, forfait)
        db.fermerdb()
        # return Response(json.dumps(eventList), mimetype='application/json')
        return Response(json.dumps("ok"), mimetype='application/json')

    else:
        return repr("Error")

# @app.route('/updateBDCorpo', methods = ["GET", "POST"])
# def updateBDCorpo():
#     if request.method == "POST":
#         tableName = request.form["tableName"]
#         colonne = request.form["colonne"]
#         valeur = request.form["valeur"]
#         _id = request.form["_id"]
#         db = Dbman()
#         db.updateDB(tableName, colonne, valeur, _id)


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


@app.route('/newLivrable', methods=["GET", "POST"])
def newLivrable():
    if request.method == "POST":
        pass
    else:
        return repr("Error")


@app.route('/deleteLivrable', methods=["GET", "POST"])
def deleteLivrable():
    if request.method == "POST":
        pass
    else:
        return repr("Error")


@app.route('/updateLivrable', methods=["GET", "POST"])
def updateLivrable():
    if request.method == "POST":
        pass
    else:
        return repr("Error")


@app.route('/getLivrable', methods=["GET", "POST"])
def getLivrable():
    if request.method == "POST":
        db = Dbclient()
        events = db.getEvent()
        db.fermerdb()
        return Response(json.dumps(events), mimetype='application/json')
    else:
        return repr("pas ok")


if __name__ == '__main__':
    # print(flask.__version__)
    # app.run(debug=True)
    app.run(debug=True, host='127.0.0.1', port=5000)
