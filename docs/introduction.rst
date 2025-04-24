Introduction
============

Holiday Homes est une application Django dédiée à la gestion de locations de vacances et de profils utilisateurs. Elle offre une plateforme permettant aux utilisateurs de parcourir les propriétés disponibles et de consulter les profils des utilisateurs.

Structure du projet
------------------

L'application est divisée en trois composants principaux :

1. **oc_lettings_site** : Le projet Django principal contenant les paramètres et la configuration de base.
2. **lettings** : Une application Django pour la gestion des propriétés à louer.
3. **profiles** : Une application Django pour la gestion des profils utilisateurs.

Ces composants sont organisés selon les bonnes pratiques Django, avec une séparation claire des responsabilités.

Fonctionnalités
--------------

* **Gestion des locations** : Parcourir et consulter les détails des propriétés disponibles
* **Gestion des profils** : Consulter les informations des utilisateurs inscrits
* **Interface d'administration** : Gérer les données du site via l'interface admin de Django
* **Suivi des erreurs** : Intégration avec Sentry pour la surveillance et la notification des erreurs
* **Pipeline CI/CD** : Automatisation des tests, du build et du déploiement

Technologies utilisées
---------------------

* **Backend** :
    * Python 3.9
    * Django 3.0
    * SQLite (développement)
    * PostgreSQL (production)
    
* **Déploiement** :
    * Docker
    * Render (PaaS)
    * GitHub Actions
    
* **Qualité du code** :
    * Pytest pour les tests
    * Flake8 pour le linting
    * Black pour le formatage
    * Bandit pour l'analyse de sécurité
    
* **Monitoring** :
    * Sentry pour le suivi des erreurs
    * Logging pour le diagnostic

Le projet a été conçu avec une attention particulière à la qualité du code, à la maintenabilité et à l'intégration continue. 