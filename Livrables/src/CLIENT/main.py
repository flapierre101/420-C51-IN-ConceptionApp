## -*- Encoding: UTF-8 -*-

from vue import *
from modele import *

import urllib.request
import urllib.parse 
import sys


import json 

from subprocess import Popen 
##################
class Controleur:
    def __init__(self):
        self.urlserveur="http://127.0.0.1:5000"
        #self.urlserveur= "http://jmdeschamps.pythonanywhere.com"
        self.modele=Modele(self)
        self.vue=Vue(self)
        self.vue.afficherlogin("aaa@xyz.com","AAAaaa111")
        self.vue.root.mainloop()
    
    def telechargermodule(self,fichier):
        leurl=self.urlserveur+"/telechargermodule"
        params = {"fichier":fichier}
        reptext=self.appelserveur(leurl,params)
        rep=json.loads(reptext)
        fichier1=open("./SaaS_modules/"+fichier,"w")
        fichier1.write(rep)
        fichier1.close()
        usager=json.dumps([self.modele.nom,self.modele.compagnie])
        Popen([sys.executable, "./SaaS_modules/"+fichier,self.urlserveur,usager],shell=1).pid 
                  
    def testsimple(self):
        leurl=self.urlserveur
        r=urllib.request.urlopen(leurl)
        rep=r.read()
        dict=rep.decode('utf-8')
        print("testserveurSIMPLE", dict)
    
    def trouvermodules(self): 
        url = self.urlserveur+"/trouvermodules"
        params = {}
        reptext=self.appelserveur(url,params)
        
        mondict=json.loads(reptext)
        return mondict  
    
    def trouverprojets(self): 
        url = self.urlserveur+"/trouverprojets"
        params = {}
        reptext=self.appelserveur(url,params)        
        mondict=json.loads(reptext)              
        return mondict
     
    def trouvermembres(self): 
        url = self.urlserveur+"/trouvermembres"
        params = {}
        reptext=self.appelserveur(url,params)
        
        mondict=json.loads(reptext)
        return mondict
    
    def identifierusager(self,nom,mdp): 
        url = self.urlserveur+"/identifierusager"
        params = {"nom":nom,
                  "mdp":mdp}
        reptext=self.appelserveur(url,params)
        
        mondict=json.loads(reptext)        
        if "inconnu" in mondict:
            self.vue.avertirusager("Erreur","Mot de passe ou identifiant non reconnnu \n\nReesayer?")
        else:            
            self.modele.inscrireusager(mondict)
            self.vue.creercadreprincipal(self.modele)
            self.vue.changercadre("principal")

    # fonction d'appel normalisee, utiliser par les methodes du controleur qui communiquent avec le serveur
    def appelserveur(self,url,params):
        query_string = urllib.parse.urlencode( params )
        data = query_string.encode( "ascii" )
        url = url + "?" + query_string 
        rep=urllib.request.urlopen(url , data)
        reptext=rep.read()
        return reptext
    
if __name__ == '__main__':
    c=Controleur()
    print("FIN DE PROGRAMME")