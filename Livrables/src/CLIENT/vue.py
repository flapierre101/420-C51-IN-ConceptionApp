from tkinter import *
from tkinter.simpledialog import *
from tkinter import ttk


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()

        # le cadre qui va afficher ou non tous les autres
        self.cadreapp = Frame(self.root)
        self.cadres = {}
        self.cadreapp.pack()
        self.cadreactif = None
        self.creercadres()

    def changercadre(self, nomcadre):
        cadre = self.cadres[nomcadre]
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif = cadre
        self.cadreactif.pack()
        if (nomcadre == "principal"):
            self.gerermodules()

    def creercadres(self):
        self.cadres["login"] = self.creercadrelogin()

    def creercadrelogin(self):
        self.cadrelogin = Frame(self.cadreapp, width=800, height=400)

        self.loginlabel = Label(self.cadrelogin, text="Identification pour Production CDJ", font=("Arial", 18),
                                borderwidth=2, relief=GROOVE)

        self.loginlabnom = Label(
            self.cadrelogin, text="Nom", font=("Arial", 14))
        self.loginnom = Entry(self.cadrelogin, font=("Arial", 14), width=30)
        self.loginlabmdp = Label(
            self.cadrelogin, text="MotdePasse", font=("Arial", 14))
        self.loginmdp = Entry(self.cadrelogin, font=(
            "Arial", 14), show="*", width=30)

        # les boutons d'actions
        self.btnannulerlogin = Button(self.cadrelogin, text="Annuler", font=(
            "Arial", 12), padx=10, pady=10, command=self.annulerlogin)
        self.btnidentifierlogin = Button(self.cadrelogin, text="Identifier", font=(
            "Arial", 12), padx=10, pady=10, command=self.identifierlogin)

        self.loginlabel.grid(row=10, column=10, columnspan=20,
                             padx=10, pady=10, ipadx=10, ipady=10)
        self.loginlabnom.grid(row=20, column=10, sticky=E, padx=5, pady=5)
        self.loginnom.grid(row=20, column=20, padx=10, pady=5)
        self.loginlabmdp.grid(row=30, column=10, sticky=E, padx=5, pady=5)
        self.loginmdp.grid(row=30, column=20, padx=10, pady=5)

        self.btnannulerlogin.grid(
            row=40, column=20, sticky=W, padx=10, pady=10)
        self.btnidentifierlogin.grid(row=40, column=20, padx=10, pady=10)

        return self.cadrelogin


    def gererforfait(self, msg = ""):
        self.modulevisible = False
        self.creercadreforfait(self.parent.getcompagnie(), msg)
        self.changercadre("forfait")

    def creercadreforfait(self, compagnie, msg):
        self.root.title("Production CDJ")
        self.cadreforfait = Frame(self.cadreapp, width=400, height=400)

        self.cadretitre = Frame(self.cadreforfait, width=400, height=400)

        if compagnie["forfait"] == 1:
            forfait = "Gratuit"
        elif compagnie["forfait"] == 2:
            forfait = "Pro"
        else:
            forfait = "Entreprise"

        if(msg == ""):
            self.forfaitlabel = Label(self.cadretitre, text="Le forfait actuel pour votre compagnie est : " + forfait, font=("Arial", 14))
        else:
            self.forfaitlabel = Label( self.cadretitre, text="Votre nouveau forfait est : " + forfait, font=("Arial", 14))
        self.forfaitlabel.pack()
        self.cadretitre.pack(pady=40)

        self.cadrecontenu = Frame(self.cadreforfait, width=600, height=400)
        text_widget = Text(self.cadrecontenu, height=28, width=60)
        text_widget.pack()
        text_widget.insert(END, "Les avantages de chacun des forfaits \n\nBase (Gratuit) : \n " +
                           "- Gestion des évènements de base\n - Liste des employés\n - Gestion des échéanciers et livrables\n - Base de données pour vos clients (limite 500)" +
                           "\n\nPro (300$\\année)\n - Module de gestions des réunions \n - Template d'évènement \n - Base de données clients limite de 1500 clients" +
                           "\n\nEntreprise (600$\\année)\n - Nombre de clients illimités et rapport sur mesure\n - Module finance\n - Module gestion de la sous-traitance" +
                           "\n - Module campagne publicitaire\n - Module de gestion d'inventaire")

        text_widget.config(state=DISABLED)

        btnsaction = []

        btnsaction.append(Button(self.cadrecontenu, text="Retour",
                                 font=("Arial", 12), padx=10, pady=10, command=lambda: self.changercadre("principal")))
        if compagnie["forfait"] > 1:
            btnsaction.append(Button(self.cadrecontenu, text="Downgrade Gratuit",
                                     font=("Arial", 12), padx=10, pady=10, command=lambda: self.changerforfait(1)))
        if compagnie["forfait"] > 2:
            btnsaction.append(Button(self.cadrecontenu, text="Downgrade Pro",
                                     font=("Arial", 12), padx=10, pady=10, command=lambda: self.changerforfait(2)))
        if compagnie["forfait"] < 2:
            btnsaction.append(Button(self.cadrecontenu, text="Upgrader à PRO",
                                     font=("Arial", 12), padx=10, pady=10, command=lambda: self.changerforfait(2)))
        if compagnie["forfait"] < 3:
            btnsaction.append(Button(self.cadrecontenu, text="Upgrader à Entreprise",
                                     font=("Arial", 12), padx=10, pady=10, command=lambda: self.changerforfait(3)))

        for i in btnsaction:
            i.pack(side=LEFT, pady=10, padx=10)

        self.cadrecontenu.pack()
        self.cadrepied = Frame(self.cadreforfait, width=600, height=80)
        self.cadrepied.pack()

        self.cadres["forfait"] = self.cadreforfait

    def changerforfait(self, forfait):
        rep = self.parent.changerForfait(forfait)
        if rep == "ok":
            self.gererforfait(rep)

    def creercadreprincipal(self, usager):
        self.root.title("Production CDJ")

        self.cadreprincipal = Frame(self.cadreapp, width=400, height=400)

        self.cadretitre = Frame(self.cadreapp, width=400, height=400)
        self.titreprincipal = Label(self.cadretitre, text="Production CDJ"+" pour "+usager.compagnie["nom"], font=("Arial", 18),
                                    borderwidth=2, relief=GROOVE)

        self.usagercourant = Label(
            self.cadretitre, text=usager.nom+" "+usager.prenom + " : "+usager.role, font=("Arial", 14))
        self.titreprincipal.pack()
        self.usagercourant.pack()
        self.cadretitre.pack()

        # commande possible
        self.cadrecommande = Frame(self.cadreprincipal, width=400, height=400)
        btnsaction = []
        if usager.droit == "Admin":
            btnsaction.append(Button(self.cadrecommande, text="Gestion de membres",
                                     font=("Arial", 12), padx=10, pady=10, command=self.gerermembres))
            btnsaction.append(Button(self.cadrecommande, text="Forfaits",
                                     font=("Arial", 12), padx=10, pady=10, command=self.gererforfait)),
        btnsaction.append(Button(self.cadrecommande, text="Modules",
                                 font=("Arial", 12), padx=10, pady=10, command=self.gerermodules))
        for i in btnsaction:
            i.pack(side=LEFT, pady=10, padx=10)
        self.cadrecommande.pack()
        self.cadrecontenu = Frame(
            self.cadreprincipal, width=600, height=400, bg="green")
        self.cadrecontenu.pack()
        self.cadrepied = Frame(self.cadreprincipal, width=600, height=80)
        self.cadrepied.pack()

        # Sauvegarder l'usager
        self.usager = usager
        self.creertableau()
        self.modulevisible = False
        self.cadres["principal"] = self.cadreprincipal

    def creertableau(self):
        f = Frame(self.cadrecontenu)
        f.pack(side=TOP, fill=BOTH, expand=Y)

        self.tableau = ttk.Treeview(show='headings')

        self.tableau.bind("<Double-1>", self.affichertelecharger)

        ysb = ttk.Scrollbar(orient=VERTICAL, command=self.tableau.yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command=self.tableau.xview)
        self.tableau['yscroll'] = ysb.set
        self.tableau['xscroll'] = xsb.set

        # add tableau and scrollbars to frame
        self.tableau.grid(in_=f, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=f, row=0, column=1, sticky=NS)
        xsb.grid(in_=f, row=1, column=0, sticky=EW)

        # set frame resize priorities
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)

    def affichertelecharger(self, evt):
        if self.modulevisible:
            item = self.tableau.selection()
            for i in item:
                fichier = self.dictlisteformatee[self.tableau.item(i, "values")[
                    0]]
            self.parent.telechargermodule(fichier)

    def ecriretableau(self):
        for i in self.tableau.get_children():
            self.tableau.delete(i)
        for item in self.data:
            if isinstance(item, str):
                item = [item]
            self.tableau.insert('', 'end', values=item)

    def integretableau(self, listemembre, entete):
        self.data = listemembre
        self.colonnestableau = entete

        self.tableau.config(columns=self.colonnestableau)
        n = 1
        for i in self.colonnestableau:
            no = "#"+str(n)
            self.tableau.heading(no, text=i)
            n += 1

        self.ecriretableau()

    def afficherlogin(self, nom="", mdp=""):
        self.root.title("GestMedia: Identification")
        if nom:
            self.loginnom.insert(0, nom)
        if mdp:
            self.loginmdp.insert(0, mdp)
        self.loginnom.focus_set()
        self.changercadre("login")

    def gerermembres(self):
        self.modulevisible = False
        listemembres = self.parent.trouvermembres()
        entete = ["Nom", "courriel", "Rôle", "Droit d'accès"]
        self.integretableau(listemembres, entete)

    def gerermodules(self):
        self.modulevisible = True
        listemodules = self.parent.trouvermodules()
        self.dictlisteformatee = {}
        compagnie = self.parent.getcompagnie()
        for module in listemodules:

            forfaitrequis = module[:1]
            if int(compagnie["forfait"])-1 >= int(forfaitrequis):
                moduleformate = module[2:-3]
                moduleformate = moduleformate.replace("_", " ")
                moduleformate = moduleformate.capitalize()
                # Creer un dictionnaire avec le nom réel du fichier sur le serveur, la clé étant le nom formaté :
                self.dictlisteformatee[moduleformate] = module

        entete = ["modules disponibles"]
        self.integretableau(self.dictlisteformatee.keys(), entete)

    def annulerlogin(self):
        self.root.destroy()

    def identifierlogin(self):
        nom = self.loginnom.get()
        mdp = self.loginmdp.get()
        self.parent.identifierusager(nom, mdp)

    def avertirusager(self, titre, message):
        rep = messagebox.askyesno(titre, message)
        if not rep:
            self.root.destroy()

    def centrerfenetre(self):
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        # get screen width and height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/3) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
