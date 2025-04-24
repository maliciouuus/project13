Déploiement
==========

Cette section explique comment déployer l'application Holiday Homes en production.

Pipeline CI/CD
-------------

Le projet utilise GitHub Actions pour implémenter un pipeline CI/CD. Le workflow est défini dans le fichier `.github/workflows/ci-cd.yml` et comprend :

1. **Test** : Exécution des tests et vérification de la qualité du code
2. **Vérification de sécurité** : Analyse du code et des dépendances pour détecter les vulnérabilités
3. **Documentation** : Génération de la documentation Sphinx
4. **Construction et publication Docker** : Création d'une image Docker et publication sur DockerHub
5. **Déploiement** : Déploiement de l'application sur Render
6. **Validation du déploiement** : Vérification que l'application est bien en ligne

Secrets GitHub requis
--------------------

Pour configurer le pipeline CI/CD, vous devez ajouter les secrets suivants dans votre dépôt GitHub :

* `DOCKERHUB_USERNAME` : Votre nom d'utilisateur DockerHub
* `DOCKERHUB_TOKEN` : Votre token d'accès DockerHub
* `RENDER_DEPLOY_HOOK_URL` : URL du webhook de déploiement Render
* `DEPLOYMENT_URL` : URL de votre application déployée

Vous pouvez également utiliser l'API Render avec ces secrets :

* `RENDER_API_KEY` : Votre clé API Render
* `RENDER_SERVICE_ID` : L'ID de votre service Render

Déploiement sur Render
---------------------

L'application est configurée pour être déployée sur Render via le fichier `render.yaml`, qui définit :

* Le type et la configuration du service
* Les commandes de build et de démarrage
* Les variables d'environnement
* Les paramètres de déploiement

### Déploiement manuel sur Render

1. Créez un compte sur [Render](https://render.com)
2. Créez un nouveau service Web
3. Connectez-le à votre dépôt GitHub
4. Utilisez les paramètres suivants :
   * **Framework** : Python
   * **Runtime** : Python 3.9
   * **Build Command** : `pip install -r requirements.txt`
   * **Start Command** : `gunicorn oc_lettings_site.wsgi:application`

5. Configurez les variables d'environnement requises :
   * `DEBUG` : Mettre à "False" pour la production
   * `SECRET_KEY` : Générer une clé secrète sécurisée
   * `SENTRY_DSN` : Votre DSN Sentry pour le suivi des erreurs
   * `SENTRY_ENVIRONMENT` : Mettre à "production"
   * `RENDER` : Mettre à "True" pour activer les paramètres de production
   * `DATABASE_URL` : URL de connexion à votre base de données PostgreSQL (si utilisée)

6. Déployez le service

### Déploiement automatique avec le fichier render.yaml

Si vous utilisez le fichier `render.yaml` fourni, vous pouvez configurer un déploiement automatique sur Render :

1. Connectez-vous à votre compte Render
2. Allez dans la section "Blueprints"
3. Cliquez sur "New Blueprint Instance"
4. Sélectionnez votre dépôt GitHub
5. Render détectera automatiquement le fichier `render.yaml` et configurera les services en conséquence
6. Ajoutez les variables d'environnement requises qui ne sont pas dans le fichier YAML
7. Cliquez sur "Apply" pour déployer

Paramètres de production
----------------------

Les paramètres spécifiques à la production sont définis dans `oc_lettings_site/settings_prod.py`, qui active :

* Paramètres HTTPS sécurisés
* Configuration adaptée de la base de données
* Logging approprié pour la production
* Suivi des erreurs Sentry avec l'environnement de production

Gestion des bases de données
--------------------------

Ce projet utilise exclusivement SQLite, même en production. Voici comment gérer correctement SQLite en production :

1. **Sauvegarde régulière** : Configurez des sauvegardes régulières du fichier `oc-lettings-site.sqlite3`
2. **Emplacement sécurisé** : Assurez-vous que le fichier de base de données est stocké dans un volume persistant
3. **Permissions** : Vérifiez que les permissions du fichier permettent à l'application d'y accéder en lecture/écriture
4. **Migrations** : Les migrations sont exécutées automatiquement lors du déploiement grâce à la commande `preDeployCommand` dans `render.yaml`

Avantages de cette approche :
* Simplicité de configuration et de maintenance
* Pas de service de base de données distinct à gérer
* Cohérence entre les environnements de développement et de production

Surveillance et journalisation
----------------------------

Une fois l'application déployée, surveillez son fonctionnement à l'aide de :

* **Sentry** : Pour le suivi des erreurs et des performances
* **Logs Render** : Accessibles via l'interface Render
* **Métriques Render** : Pour surveiller l'utilisation des ressources

En cas de problème lors du déploiement
------------------------------------

Si vous rencontrez des problèmes lors du déploiement :

1. Vérifiez les logs de déploiement sur Render
2. Assurez-vous que toutes les variables d'environnement sont correctement configurées
3. Vérifiez que le fichier `requirements.txt` inclut toutes les dépendances nécessaires
4. Testez l'application localement avec les paramètres de production :
   ```bash
   RENDER=True python manage.py runserver
   ```
5. Vérifiez les permissions du fichier de base de données SQLite
6. Examinez les logs d'erreur dans Sentry 