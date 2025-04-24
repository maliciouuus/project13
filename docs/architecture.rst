Architecture
============

Cette section décrit l'architecture du projet Holiday Homes.

Structure du projet
----------------

Le projet est organisé en plusieurs composants principaux :

* **oc_lettings_site** : Projet Django principal
* **lettings** : Application pour la gestion des locations
* **profiles** : Application pour la gestion des profils utilisateurs

.. code-block:: bash

   project13/
   ├── .github/                 # Configuration GitHub Actions
   ├── docs/                    # Documentation Sphinx
   ├── lettings/                # Application de gestion des locations
   │   ├── migrations/          # Migrations de base de données
   │   ├── templates/           # Templates spécifiques aux locations
   │   ├── admin.py             # Configuration de l'interface d'administration
   │   ├── apps.py              # Configuration de l'application
   │   ├── models.py            # Définition des modèles de données
   │   ├── tests.py             # Tests unitaires
   │   ├── urls.py              # Configuration des URLs
   │   └── views.py             # Vues de l'application
   ├── oc_lettings_site/        # Configuration principale du projet
   │   ├── utils/               # Utilitaires partagés
   │   ├── settings.py          # Paramètres de développement
   │   ├── settings_prod.py     # Paramètres de production
   │   ├── urls.py              # Configuration des URLs principales
   │   ├── views.py             # Vues principales
   │   └── wsgi.py              # Configuration WSGI
   ├── profiles/                # Application de gestion des profils
   │   ├── [structure similaire à lettings]
   ├── static/                  # Fichiers statiques (CSS, JS, images)
   ├── templates/               # Templates partagés
   ├── .coveragerc              # Configuration de la couverture des tests
   ├── .env.example             # Exemple de fichier de variables d'environnement
   ├── .flake8                  # Configuration du linting
   ├── conftest.py              # Configuration pytest
   ├── docker-compose.yml       # Configuration Docker Compose
   ├── Dockerfile               # Instructions de build Docker
   ├── manage.py                # Script de gestion Django
   ├── pytest.ini               # Configuration pytest
   ├── README.md                # Documentation principale
   ├── render.yaml              # Configuration de déploiement Render
   └── requirements.txt         # Dépendances du projet

Modèle de données
----------------

Le schéma de base de données du projet est organisé autour de quatre entités principales :

* **User** : Modèle standard de Django pour l'authentification des utilisateurs
* **Profile** : Extension du modèle User avec des informations supplémentaires
* **Address** : Représentation d'une adresse physique
* **Letting** : Représentation d'une propriété en location

.. raw:: html

   <div class="mermaid">
   classDiagram
       class User {
           +id: AutoField (PK)
           +username: CharField
           +email: EmailField
           +password: CharField
           +first_name: CharField
           +last_name: CharField
           +is_active: BooleanField
           +is_staff: BooleanField
           +is_superuser: BooleanField
           +date_joined: DateTimeField
           +last_login: DateTimeField
       }
       
       class Profile {
           +id: AutoField (PK)
           +user: OneToOneField (FK)
           +favorite_city: CharField
           +__str__(): String
       }
       
       class Address {
           +id: AutoField (PK)
           +number: PositiveIntegerField
           +street: CharField
           +city: CharField
           +state: CharField
           +zip_code: PositiveIntegerField
           +country_iso_code: CharField
           +__str__(): String
       }
       
       class Letting {
           +id: AutoField (PK)
           +title: CharField
           +address: OneToOneField (FK)
           +__str__(): String
       }
       
       User "1" -- "1" Profile : has
       Address "1" -- "1" Letting : belongs to
   </div>

Relations
^^^^^^^^^

* Un utilisateur (User) a exactement un profil (Profile) - Relation OneToOne
* Une adresse (Address) est associée à exactement une location (Letting) - Relation OneToOne

Cette structure modulaire permet une séparation claire des préoccupations entre la gestion des utilisateurs (profiles) et la gestion des propriétés (lettings), conformément aux principes de conception de Django.

Structure des URLs
---------------

* `/` : Page d'accueil
* `/lettings/` : Liste de toutes les locations
* `/lettings/<id>/` : Détails d'une location spécifique
* `/profiles/` : Liste de tous les profils utilisateurs
* `/profiles/<username>/` : Détails d'un profil utilisateur spécifique
* `/admin/` : Interface d'administration
* `/sentry-test/` : Point d'accès de test pour Sentry

Couche de vues
------------

Les vues sont organisées par application :

* `oc_lettings_site/views.py` : Vues principales, y compris la page d'accueil et les gestionnaires d'erreurs
* `lettings/views.py` : Vues pour parcourir les locations
* `profiles/views.py` : Vues pour parcourir les profils

Le projet utilise le système de templates de Django avec les templates stockés dans :

* `templates/` : Templates partagés (base, index, erreurs)
* `lettings/templates/` : Templates spécifiques aux locations
* `profiles/templates/` : Templates spécifiques aux profils

Gestion des erreurs
----------------

L'application inclut :

* Gestionnaires d'erreurs 404 et 500 personnalisés
* Intégration de Sentry pour la surveillance des erreurs
* Utilitaires de journalisation dans `oc_lettings_site/utils/logging_utils.py`

Les erreurs sont capturées et enregistrées à plusieurs niveaux :

1. **Niveau application** : Toutes les vues utilisent des décorateurs pour journaliser les appels de fonction et les erreurs
2. **Niveau Django** : Configuration de journalisation Django dans settings.py
3. **Niveau Sentry** : Capture des erreurs non gérées et des messages explicites

Architecture de déploiement
------------------------

En production, l'application est déployée :

* Comme un conteneur Docker
* Sur la plateforme cloud Render
* Avec une base de données PostgreSQL (si configurée)
* Derrière HTTPS
* Avec Sentry pour le suivi des erreurs

Le diagramme suivant illustre l'architecture de déploiement :

.. code-block::

                                    ┌───────────────┐
                                    │   GitHub      │
                                    │  Repository   │
                                    └───────┬───────┘
                                            │
                                            ▼
    ┌──────────────┐              ┌─────────────────┐
    │              │              │  GitHub Actions │
    │  Developer   ├─────────────►│     CI/CD       │
    │              │              │    Pipeline     │
    └──────────────┘              └────────┬────────┘
                                           │
                                           │
                   ┌─────────────┬─────────┴──────────┬──────────────┐
                   │             │                    │              │
                   ▼             ▼                    ▼              ▼
           ┌───────────┐  ┌────────────┐     ┌───────────────┐ ┌────────────┐
           │ Run Tests │  │ Build Docs │     │Docker Registry│ │   Render   │
           └───────────┘  └────────────┘     └───────┬───────┘ └──────┬─────┘
                                                     │                │
                                                     │                │
                                                     ▼                ▼
                                            ┌─────────────────────────────┐
                                            │      Production Server      │
                                            └──────────────┬──────────────┘
                                                           │
                                                           │
                                          ┌────────────────┴─────────────┐
                                          │                              │
                                          ▼                              ▼
                                  ┌───────────────┐             ┌────────────────┐
                                  │ PostgreSQL DB │             │ Sentry         │
                                  └───────────────┘             └────────────────┘

Ce diagramme montre comment le code passe du développeur au déploiement en production à travers le pipeline CI/CD. 