Déploiement
==========

Cette section explique comment déployer l'application Holiday Homes en production.

Pipeline CI/CD avec GitHub Actions
-------------

Notre projet utilise un workflow GitHub Actions pour automatiser la construction et le déploiement de l'application. Le workflow est défini dans le fichier `.github/workflows/docker-build.yml` et fonctionne comme suit :

1. **Construction et publication de l'image Docker** :
   - À chaque push sur la branche main, GitHub Actions déclenche la construction d'une image Docker
   - Cette image est publiée automatiquement sur Docker Hub avec le tag `purityoff/oc-lettings:latest`
   - Le processus est entièrement automatisé et ne nécessite aucune intervention manuelle

2. **Déploiement automatique sur Render** :
   - Render est configuré pour surveiller l'image Docker sur Docker Hub
   - Dès qu'une nouvelle version de l'image est publiée, Render la détecte automatiquement
   - Render télécharge et déploie la nouvelle image sans intervention manuelle

Ce workflow simplifié présente plusieurs avantages :
   - Déploiements rapides et fiables
   - Traçabilité complète (chaque version déployée correspond à une image Docker spécifique)
   - Séparation claire entre la construction (GitHub Actions) et le déploiement (Render)

Secrets GitHub requis
--------------------

Pour configurer le pipeline CI/CD, vous devez ajouter les secrets suivants dans votre dépôt GitHub :

* ``DOCKER_USERNAME`` : Votre nom d'utilisateur DockerHub (purityoff)
* ``DOCKER_PASSWORD`` : Votre token d'accès DockerHub

Configuration de Render
---------------------

Pour déployer l'application sur Render, suivez ces étapes :

1. Créez un compte sur `Render <https://render.com>`_
2. Créez un nouveau service Web
3. Sélectionnez "Docker" comme type de service
4. Dans les paramètres du service :
   * **Name** : Nom de votre service (par exemple, "holiday-homes")
   * **Image URL** : ``docker.io/purityoff/oc-lettings:latest``
   * **Pull Command** : ``docker pull purityoff/oc-lettings:latest``
   * **Instance Type** : Choisissez le type adapté à vos besoins (Free tier pour les tests)
   * **Disk** : Assurez-vous d'avoir suffisamment d'espace disque pour la base de données SQLite

5. Configurez les variables d'environnement requises :
   * ``DEBUG`` : ``False`` pour la production
   * ``SECRET_KEY`` : Générer une clé secrète sécurisée
   * ``SENTRY_DSN`` : Votre DSN Sentry pour le suivi des erreurs
   * ``ALLOWED_HOSTS`` : Votre domaine Render (par exemple, ``project13-r64u.onrender.com``)

6. Cliquez sur "Create Web Service"

Base de données locale SQLite
----------------------------

Cette application utilise SQLite comme base de données, même en production. Les avantages de cette approche sont :

1. **Simplicité** : Pas besoin de configurer un service de base de données externe
2. **Portabilité** : La base de données est un simple fichier, facile à sauvegarder
3. **Cohérence** : Même environnement de développement et de production

Le fichier de base de données SQLite (`oc-lettings-site.sqlite3`) est stocké dans le volume persistant de Render, 
ce qui garantit que les données sont conservées entre les redémarrages et les déploiements.

**Important** : Pour les applications à fort trafic, cette approche pourrait ne pas être adaptée. 
Dans ce cas, envisagez de migrer vers PostgreSQL ou un autre système de gestion de base de données relationnel plus robuste.

Modifications et redéploiement
-----------------------------

Pour modifier l'application et la redéployer :

1. Effectuez vos modifications dans le code (par exemple, changer le titre dans index.html)
2. Committez et poussez les modifications sur la branche main :

   .. code-block:: bash

      git add .
      git commit -m "Update title in index.html"
      git push origin main

3. GitHub Actions construira automatiquement une nouvelle image Docker
4. Render détectera la nouvelle image et la déploiera automatiquement
5. En quelques minutes, vos modifications seront visibles sur le site déployé

Test de l'image Docker en local
-----------------------------

Pour tester l'image Docker localement avant déploiement :

.. code-block:: bash

   # Extraire l'image depuis Docker Hub
   docker pull purityoff/oc-lettings:latest

   # Exécuter l'image localement
   docker run -p 8000:8000 --env-file .env purityoff/oc-lettings:latest

L'application sera accessible à l'adresse http://localhost:8000/

Surveillance et journalisation
----------------------------

Une fois l'application déployée, surveillez son fonctionnement à l'aide de :

* **Sentry** : Pour le suivi des erreurs et des performances
* **Logs Render** : Accessibles via l'interface Render (Dashboard > Your Service > Logs)
* **Métriques Render** : Pour surveiller l'utilisation des ressources

En cas de problème lors du déploiement
------------------------------------

Si vous rencontrez des problèmes lors du déploiement :

1. Vérifiez les logs de déploiement sur Render
2. Assurez-vous que toutes les variables d'environnement sont correctement configurées
3. Vérifiez que l'image Docker a bien été publiée sur Docker Hub
4. Testez l'image Docker localement pour vérifier qu'elle fonctionne correctement
5. Examinez les logs d'erreur dans Sentry 