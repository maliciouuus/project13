Introduction
============

Présentation du projet
---------------------

OC Lettings est une application web Django développée pour Orange County Lettings, une startup dans le domaine de la location immobilière en pleine expansion aux États-Unis.

Ce projet est une refonte d'une application monolithique existante, réorganisée en une architecture modulaire plus maintenable.

Objectifs du projet
------------------

L'application a été améliorée pour répondre aux besoins suivants:

* Refactorisation en architecture modulaire avec applications séparées
* Mise en place d'une surveillance des erreurs avec Sentry
* Déploiement via un pipeline CI/CD automatisé
* Conteneurisation avec Docker
* Documentation technique complète

Technologies utilisées
---------------------

* **Backend:** Django 3.2
* **Base de données:** SQLite (développement), PostgreSQL (production)
* **Surveillance des erreurs:** Sentry
* **CI/CD:** GitHub Actions
* **Conteneurisation:** Docker
* **Déploiement:** Render
* **Documentation:** Sphinx 