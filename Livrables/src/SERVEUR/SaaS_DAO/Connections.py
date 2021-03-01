import os
import sqlite3

class Connections:
    def __init__(self):
        self.clientGestion = None
        self.clientProjet = None

    def getConnectionDBGestion(self):
        if self.clientGestion is None:
            try:
                dbString = os.getcwd()+"/SaaS_DB/"+"Production_CDJ_corpo.sqlite"
                self.clientGestion = sqlite3.connect(dbString)
                return self.clientGestion
            except:
                self.clientGestion = None
            finally:
                pass


    def getConnectionDBProjet():
        pass