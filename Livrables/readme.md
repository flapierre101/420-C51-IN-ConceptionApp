### Auteurs : Dany Viens, Caroline Emond-Serret, François Lapierre

# Readme créé le xx xx xx


Ce document est disponible sous forme .txt et .md
Pour une meilleure visualisation, utilisez le format .md

Document .txt disponible pour le résumé des scrums et de la plannification de chacun de nos sprints.


Information sur l'état du logiciel
Indications sommaires d'usage
Avertissements -(IE : ce qui ne fonctionnement pas)


# Introduction

### 
    Nous avons choisi d'implanter un logiciel de gestion d'évènement : festival, musique, spectacle, etc.


    L'objectif du logiciel est d'offrir différents modules permettent de gérer la préparation à un évènement, mais également d'aider à gérer les clients participants à l'évènement.


    Listes des modules souhaités : gestion évènement, gestion des employés


## Modèle d'affaire

### 
    Nous avons choisi d'utiliser un modèle d'affaire de type "Freemium"

    Le modèle freemium permet aux utilisateurs d'utiliser gratuitement les fonctions de base d'un logiciel, puis de payer pour des "mises à niveau" du paquet de bases. Il s'agit d'une tactique populaire pour les entreprises qui débutent et qui tentent d'attirer les utilisateurs vers leur logiciel ou service.

    - Le modèle d'affaires comporte trois niveaux de forfait : 
        - Base, pro et entreprise
        - Chaque forfait donne accès à différents modules ou des fonctionnalités plus avancées
    - Est basé sur un montant annuel X pour les clients.
    


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
    - Changer le visuel

## Fonctionnement module gestion d'événement

- Introduction: Module central permettant la gestion d'événements. Ce module permettra d'associer des éléments de d'autres modules afin de planifier un événement du début à la fin.

- Général
    - Affiche la liste des événements en cours
    - Permet la création d'un nouvel événement
    - Permet de consulter les détails d'un événements et de le modifier.

- Détaillé
    -

- Avertissements - problèmes connus
    - Verification des permissions d'utilisateurs

- Fonctionnalités non implémentées et à venir:
    - Une interface permettant de lié des livrables, des clients, des utilisateurs/employés, des échéanciers, etc... Ainsi voir tous les éléments d'un événement au même endroit.


## Fonctionnement module gestion de client

- Introduction: Module permettant de faire la gestion des clients de la compagnie.

- Général
    - affichage de la liste des clients
    - ajout de nouveau clients
    - supression de client existant
    - À venir: modification d'une client existant

- Avertissements - problèmes connus
    - Disposition du UI temporaire. Rafinement à venir

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

- Détaillé
    - Possibilité d'afficher les livrables complété ou non complété.
    - Dans l'écran "Détail du livrable", il est possible d'indiquer que le livrable est complété.

- Avertissements - problèmes connus
    - Si l'on ne choisit pas de livrables avant de cliquer sur "detail", le logiciel affichera une erreur.

- Fonctionnalités non implémentées
    - Afficher le détail de l'échéancier ou de l'évènement associé au livrable
    - Créer un nouveau livrable
        -Drop-down menu pour l'évènement et l'échéancier associé.
    - Afficher les livrables par évènement.

## Fonctionnement module gestion d'utilisateur

- Introduction


- Général


- Détaillé

- Avertissements - problèmes connus

- Fonctionnalités non implémentées
