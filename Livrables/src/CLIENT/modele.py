class Modele():
    def __init__(self,parent):
        self.parent=parent 
    
    def inscrireusager(self,dictinfo, courriel):
        self.droit=dictinfo[0][0][7]
        self.role=dictinfo[0][0][6]
        self.nom=dictinfo[0][0][4]
        self.prenom=dictinfo[0][0][3]    
        self.compagnie={"nom":dictinfo[1][0][1],"responsable":dictinfo[1][0][2],
                         "forfait": dictinfo[1][0][4], "nbUsagers": dictinfo[1][0][5], "id": dictinfo[1][0][0]}
        self.courriel = courriel
