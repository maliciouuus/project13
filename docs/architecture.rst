Architecture
============

Vue d'ensemble
------------

OC Lettings est organisé en trois applications Django distinctes:

1. **oc_lettings_site**: Application principale du projet
2. **lettings**: Gestion des biens immobiliers
3. **profiles**: Gestion des profils utilisateurs

Structure du projet
-----------------

.. code-block:: text

    project13/
    ├── lettings/                # Application des locations
    │   ├── models.py            # Modèles Address et Letting
    │   ├── views.py             # Vues des locations
    │   └── templates/           # Templates spécifiques
    │
    ├── profiles/                # Application des profils
    │   ├── models.py            # Modèle Profile
    │   ├── views.py             # Vues des profils
    │   └── templates/           # Templates spécifiques
    │
    ├── oc_lettings_site/        # Application principale
    │   ├── settings.py          # Configuration Django
    │   ├── urls.py              # Routes principales
    │   └── views.py             # Vue d'index
    │
    ├── templates/               # Templates partagés
    └── static/                  # Fichiers statiques

Modèles de données
----------------

Le schéma de base de données comprend trois modèles principaux:

.. mermaid::

   classDiagram
      class Address {
          +number: int
          +street: str
          +city: str
          +state: str
          +zip_code: int
          +country_iso_code: str
      }
      
      class Letting {
          +title: str
          +address: Address
      }
      
      class Profile {
          +user: User
          +favorite_city: str
      }
      
      class User {
          +username: str
          +email: str
          +password: str
      }
      
      Letting "1" -- "1" Address: has
      Profile "1" -- "1" User: belongs to

Interfaces
---------

L'application propose plusieurs interfaces:

1. **Interface publique**: 
   - Page d'accueil
   - Liste des locations
   - Détails d'une location
   - Liste des profils 
   - Détails d'un profil

2. **Interface d'administration**:
   - Gestion des locations
   - Gestion des adresses
   - Gestion des profils
   - Gestion des utilisateurs

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