class Modele():
    def __init__(self,parent):
        self.parent=parent 
    
    def inscrireusager(self,dictinfo):
        self.nom=dictinfo[0][0][4]
        self.droit=dictinfo[0][0][6]
        self.prenom=dictinfo[0][0][3]
        self.compagnie={"nom":dictinfo[1][0][0], "id":dictinfo[0][0][0]}
