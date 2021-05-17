### Auteurs : Dany Viens, Caroline Emond-Serret, François Lapierre

# Readme créé le 17 mai 2020


Ce document est disponible sous forme .txt et .md
Pour une meilleure visualisation, utilisez le format .md

Un document .txt et .md est disponible pour le résumé des scrums et de la plannification de chacun de nos sprints.


Information sur l'état du logiciel
Indications sommaires d'usage
Avertissements -(IE : ce qui ne fonctionnement pas)


# Introduction

###
    Nous avons choisi d'implanter un logiciel de gestion d'évènement : festival, musique, spectacle, etc.


    L'objectif du logiciel est d'offrir différents modules permettent de gérer la préparation à un évènement, mais également d'aider à gérer les clients participants à l'évènement.

    Pour se connecter avec un compte admin :
        - Nom: "aaa@xyz.com", Mot de Passe : "aaa"

    Pour se connecter avec un compte sans droit d'administration :
        - Nom: "bbb@xyz.com", Mot de Passe : "aaa"

## Modèle d'affaire

###
    Nous avons choisi d'utiliser un modèle d'affaire de type "Freemium"

    Le modèle freemium permet aux utilisateurs d'utiliser gratuitement les fonctions de base d'un logiciel, puis de payer pour des "mises à niveau" du paquet de bases. Il s'agit d'une tactique populaire pour les entreprises qui débutent et qui tentent d'attirer les utilisateurs vers leur logiciel ou service.

    - Le modèle d'affaires comporte trois niveaux de forfait :
        - Base, pro et entreprise
        - Chaque forfait donne accès à différents modules ou des fonctionnalités plus avancées
    - Est basé sur un montant annuel X pour les clients.

# Historique des versions:

-  Version 0.5 : 17 mai 2020 - 
-  Version 0.3 : 26 avril 2020 - Création de la version 1 du Readme.


## À venir dans les futures versions

- Module réunion
    - Permettre de créer des réunions, gestions des salles etc.
- Module campagne publicitaire
    - Garder un historique des campagnes publiciataires, garder le matériel promotionnel réunion dans un base de donnée
- Gestion des finances
    - Gestion du coût du matérial, salaire, entrée d'argent
- Module inventaire
    - Gestion de l'inventaire (nombre en stock selon catégories)
- Module Sous-traitance
    - Gestion des contrats de sous-traitance et base de données avec les différents 
    
# Étapes à suivre pour utilisation:

## Fonctionnement module général

- Introduction :
    - Ceci est le module d'introduction pour les clients.
    - Un client doit d'abord s'authentifier à l'aide de son courriel et mot de passe
- Général
    - Selon le niveau de permission que l'utilisateur possède, il sera possible de consulter :
        - La liste des modules disponibles
        - La liste des membres (admin seulement)
        - Le détail du forfait (admin seulement)


- Détaillé
    - Forfait :
        - Il est possible de choisir entre trois forfaits différents de cet écran. L'information est enregistrée automatiquemment. Des conditions s'appliquent, une facture pourrait vous être envoyée dans les cinq jours ouvrables.
        - Trois types de forfaits :
            - Gratuit, Pro, Entreprise
    - Écran "Modules"
        - La liste affiche seulement les modules approprié pour le forfait

- Avertissements - problèmes connus
    - Aucun!

- Fonctionnalités non implémentées
    - Fonction "déconnexion" pour changer d'utilisateur sans fermer le programme

## Fonctionnement module gestion d'événement

- Introduction: Module central permettant la gestion d'événements. Ce module permettra d'associer des éléments de d'autres modules afin de planifier un événement du début à la fin.

- Général
    - Affiche la liste des événements en cours
    - Permet la création d'un nouvel événement
    - Permet de consulter les détails d'un événements et de le modifier.
        - V.0.5 NOUVEAU : De cette page, il est possible de créer un nouvel échéancier pour l'évènement. 

- Avertissements - problèmes connus
    - aucun

- Fonctionnalités non implémentées et à venir:
    - Une interface permettant de lié des livrables, des clients, des utilisateurs/employés, des échéanciers, etc... Ainsi voir tous les éléments d'un événement au même endroit.




## Fonctionnement module gestion de client

- Introduction: Module permettant de faire la gestion des clients de la compagnie.

- Général
    - affichage de la liste des clients
    - ajout de nouveau clients
    - supression de client existant

- Avertissements - problèmes connus
    - Disposition du UI temporaire. Rafinement à venir
    - Verification des permissions d'utilisateurs

- Fonctionnalités non implémentées
    - Modification des informations d'un client.
    - Faire une recherche afin de trouver un client

## Fonctionnement module gestion de livrables

###
    Gestion des livrables devant être complété dans l'évènement


- Général
    - L'écran principal affiche la liste des livrables et non complété assignés à l'employé connecté
    - Peut obtenir les détails du livrable en choisant un item dans la liste et en appuyant sur le bouton "Detail"
        - Donne la description, l'état, le propriétaire, l'échéancier associé et la date limite de l'échéancier.
    - V.0.5 NOUVEAU : Possibilité de d'ajouter un livrable

- Détaillé
    - Possibilité d'afficher les livrables complété ou non complété.
    - Dans l'écran "Détail du livrable", il est possible d'indiquer que le livrable est complété.
    - V.0.5 NOUVEAU : Dans l'écran "Ajouter un livrable"
        - Sélectionner l'évènement voulu dans le menu déroulant
            - Il sera ensuite possible de sélectionner l'échéancier désiré
        - Une fois qu'un évènement valide et un échéancier valide sont choisi, le bouton "Créer" sera actif.

- Avertissements - problèmes connus
    - Si l'on ne choisit pas de livrables avant de cliquer sur "detail", le logiciel affichera une erreur.
    - V.0.5 NOUVEAU : Possibilité de créer un livrable sans ajouter de titre ou de notes. 

- Fonctionnalités non implémentées
    - Afficher le détail de l'échéancier.
    - Afficher les livrables par évènement.

## Fonctionnement module gestion d'utilisateur

- Introduction: Module permettant de faire la gestion des utilisateurs


- Général
    - Affichage de la liste des utilisateurs courants avec leurs rôles et courriels
    - Ajouter un nouvel utilisateur
    - Modifier un utilisateur existant
    - Ajouter un nouveau rôle

- Avertissements - problèmes connus
    - Fonction/route pour aller chercher les rôles existants n'est pas encore fonctionnel


- Fonctionnalités non implémentées
    - Reste à valider si utilisateur est Admin et si non, retirer certains éléments et fonctionalités
    - Modification d'un utilisateur et  ajout de rôle pas encore fait
