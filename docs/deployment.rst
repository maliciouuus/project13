Déploiement
==========

Prérequis
--------

* Un compte Docker Hub
* Un compte Render
* Un compte GitHub

Préparation
----------

1. Forker le dépôt sur GitHub
2. Configurer les secrets dans le dépôt GitHub:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`
   - `RENDER_DEPLOY_HOOK_URL`

Déploiement sur Render
--------------------

1. Créer un nouveau service Web sur Render
2. Sélectionner "Docker Registry"
3. Entrer `purityoff/oc-lettings:latest` comme Image URL
4. Configurer les variables d'environnement:

.. code-block:: text

   DEBUG=False
   SECRET_KEY=votre_clé_secrète
   ALLOWED_HOSTS=.onrender.com,votre-app.onrender.com
   SENTRY_DSN=votre_dsn_sentry

5. Activer l'option "Auto-Deploy"

Mise à jour du site
-----------------

Pour mettre à jour le site:

1. Apporter des modifications au code
2. Pousser les changements sur GitHub
3. La pipeline CI/CD déploiera automatiquement les modifications

Surveillance
----------

* Consulter les logs sur Render
* Surveiller les erreurs dans Sentry
* Vérifier le statut des builds dans GitHub Actions

Test manuel
---------

Pour vérifier le déploiement, vous pouvez:

1. Visiter le site déployé
2. Se connecter à l'interface d'administration avec:
   - **Nom d'utilisateur:** francis
   - **Mot de passe:** francis 