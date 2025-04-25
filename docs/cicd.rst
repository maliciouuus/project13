Pipeline CI/CD
==========

Cette section détaille le pipeline d'intégration et de déploiement continus (CI/CD) implémenté pour le projet Holiday Homes.

Vue d'ensemble
-------------

Le pipeline CI/CD est implémenté avec GitHub Actions et permet d'automatiser la construction, la publication et le déploiement de l'application. Le workflow est défini dans le fichier ``.github/workflows/docker-build.yml``.

.. image:: https://mermaid.ink/img/pako:eNptkc1qAyEQhV9lmEUDpZBlQO3GZNFAoAshELLovdZoNWMwrtkQ8u5V06bQdqHinO985zL6kSvFSOmNJXZLUjOltbIqwLugbkw2uvcOuRN7EoZXhAYH79BO_JjYYhDdOvhZOq0MtOiJbYJxtHvswMBmC-MkOqnVu7f-FgG_Kb5f9i3cmbrHPHjMaYKxhY2Loe2h9iCZnkNmSE9Vs5NUw9DM4JDXfLYZl4_nC7jStT1mFzUe5lVyLx9_dRIjO2EVKXk6o5Z5WdCKlvz49QVtKTyTzOSQn5OymDK_VJSu2NLRIjWUpNJVKipW1LHCtYIWqWpYcYErEUX0D1dNg1s?type=png
   :alt: Pipeline CI/CD Flow
   :align: center

Le pipeline utilise une approche simplifiée avec deux étapes principales :

1. **Construction et publication Docker**
2. **Déploiement automatique sur Render**

Job 1: Construction et publication Docker
---------------------------------------

Ce job est exécuté à chaque push sur la branche main. Il effectue les actions suivantes :

.. code-block:: yaml

   build:
     runs-on: ubuntu-latest
     
     steps:
       - name: Checkout repository
         uses: actions/checkout@v3
         
       - name: Set up Docker Buildx
         uses: docker/setup-buildx-action@v2
         
       - name: Log in to Docker Hub
         uses: docker/login-action@v2
         with:
           username: ${{ secrets.DOCKER_USERNAME }}
           password: ${{ secrets.DOCKER_PASSWORD }}
           
       - name: Build and push Docker image
         uses: docker/build-push-action@v5
         with:
           context: .
           push: true
           tags: purityoff/oc-lettings:latest

Ce job utilise plusieurs actions GitHub :
- **actions/checkout** : Récupère le code source
- **docker/setup-buildx-action** : Configure Buildx pour des builds plus efficaces
- **docker/login-action** : Authentification sur DockerHub
- **docker/build-push-action** : Construction et publication de l'image

L'image est taguée avec ``latest`` pour toujours pointer vers la dernière version.

Déploiement automatique sur Render
--------------------------------

Render est configuré pour surveiller l'image Docker sur Docker Hub. Le déploiement est entièrement automatisé :

1. Render détecte les nouvelles versions de l'image Docker
2. Render télécharge automatiquement la nouvelle image
3. Render déploie la nouvelle image sur votre service web

Pour configurer le déploiement automatique sur Render :

1. Créez un compte sur `Render <https://render.com>`_
2. Créez un nouveau service web de type Docker
3. Spécifiez l'URL de l'image : ``docker.io/purityoff/oc-lettings:latest``
4. Configurez les variables d'environnement nécessaires
5. Activez l'option "Auto-Deploy" pour les mises à jour automatiques

Avantages de cette approche
-------------------------

Cette approche de CI/CD simplifiée offre plusieurs avantages :

1. **Simplicité** : Un workflow simple et facile à comprendre
2. **Efficacité** : Déploiement rapide des modifications
3. **Fiabilité** : Processus de déploiement cohérent
4. **Traçabilité** : Chaque déploiement correspond à une image Docker spécifique
5. **Facilité de rollback** : Possibilité de revenir à une version précédente en spécifiant une image Docker plus ancienne

Configuration requise
-------------------

Pour que le pipeline fonctionne correctement, les secrets suivants doivent être configurés dans les paramètres du dépôt GitHub :

- ``DOCKER_USERNAME`` : Nom d'utilisateur DockerHub (purityoff)
- ``DOCKER_PASSWORD`` : Token d'accès DockerHub

Tester le pipeline localement
---------------------------

Vous pouvez tester le processus de déploiement localement en exécutant l'image Docker :

.. code-block:: bash

   # Extraire l'image depuis Docker Hub
   docker pull purityoff/oc-lettings:latest
   
   # Exécuter l'image localement
   docker run -p 8000:8000 --env-file .env purityoff/oc-lettings:latest

Modification et redéploiement
---------------------------

Pour apporter des modifications et les déployer :

1. Modifiez le code source
2. Committez et poussez les changements sur la branche main
3. GitHub Actions construira et publiera automatiquement une nouvelle image Docker
4. Render détectera la nouvelle image et la déploiera automatiquement

Le temps entre le push sur GitHub et le déploiement sur Render est généralement de quelques minutes.

Bonnes pratiques
--------------

Pour tirer le meilleur parti de ce pipeline CI/CD, suivez ces bonnes pratiques :

1. **Tests locaux** : Testez vos modifications localement avant de les pousser
2. **Messages de commit clairs** : Utilisez des messages descriptifs pour faciliter le suivi des changements
3. **Branches de fonctionnalité** : Développez les nouvelles fonctionnalités sur des branches séparées
4. **Pull requests** : Utilisez des pull requests pour réviser le code avant de le fusionner avec main
5. **Surveillez les déploiements** : Vérifiez les logs sur Render après chaque déploiement

Configuration du pipeline CI/CD
-------------------------------

Le pipeline CI/CD est configuré dans le fichier ``.github/workflows/ci-cd.yml``. Il comprend les étapes suivantes :

1. **Tests** : Exécution des tests unitaires, vérification de la couverture de code, et analyse de la qualité du code.
2. **Vérifications de sécurité** : Analyse du code source avec Bandit et vérification des dépendances avec Safety.
3. **Documentation** : Génération de la documentation avec Sphinx.
4. **Construction et publication de l'image Docker** : Construction de l'image Docker et publication sur DockerHub.
5. **Déploiement** : Déploiement de l'application sur Render.
6. **Validation du déploiement** : Vérification que l'application est bien en ligne après le déploiement.

Pour que le pipeline fonctionne correctement, vous devez configurer les secrets suivants dans votre dépôt GitHub :

- ``DOCKERHUB_USERNAME`` : Votre nom d'utilisateur DockerHub
- ``DOCKERHUB_TOKEN`` : Votre token d'accès DockerHub
- ``DEPLOY_HOOK_URL`` : URL du webhook de déploiement Render
- ``DEPLOYMENT_URL`` : URL de votre application déployée sur Render

Base de données
-------------

Le pipeline CI/CD est configuré pour utiliser SQLite comme base de données, ce qui simplifie le processus de déploiement. 
L'image Docker est configurée pour stocker la base de données SQLite dans un volume persistant.

Cette approche présente plusieurs avantages pour le workflow CI/CD :

1. **Simplicité** : Pas besoin de configurer une base de données externe pour le déploiement
2. **Rapidité** : Le processus de déploiement est plus rapide car il n'y a pas de migration vers une base de données externe
3. **Cohérence** : Les mêmes tests fonctionnent de la même manière dans tous les environnements 