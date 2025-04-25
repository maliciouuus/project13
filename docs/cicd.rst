Pipeline CI/CD
============

Présentation
-----------

Le projet utilise GitHub Actions pour automatiser le processus d'intégration continue et de déploiement continu.

Étapes de la pipeline
-------------------

1. **Test**:
   - Exécution de flake8 pour la vérification du code
   - Exécution des tests pytest avec une couverture minimale de 80%

2. **Build**:
   - Construction de l'image Docker
   - Publication sur Docker Hub avec les tags `latest` et le hash du commit

3. **Déploiement**:
   - Déploiement automatique sur Render

Diagramme de flux
---------------

.. mermaid::

   graph LR
       A[Push Code] --> B[Run Tests]
       B -->|Success| C[Build Docker Image]
       C --> D[Push to Docker Hub]
       D --> E[Deploy to Render]
       B -->|Failure| F[Notify Failure]

Configuration
-----------

La configuration se trouve dans `.github/workflows/docker-build.yml`.

Variables d'environnement requises:

* `DOCKER_USERNAME`: Nom d'utilisateur Docker Hub
* `DOCKER_PASSWORD`: Mot de passe Docker Hub
* `RENDER_DEPLOY_HOOK_URL`: URL du webhook de déploiement Render

Commandes utiles
--------------

Pour tester l'image localement:

.. code-block:: bash

   docker pull purityoff/oc-lettings:latest
   docker run -p 8000:8000 --env-file .env purityoff/oc-lettings:latest

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

Bonnes pratiques
--------------

Pour tirer le meilleur parti de ce pipeline CI/CD, suivez ces bonnes pratiques :

1. **Tests locaux** : Testez vos modifications localement avant de les pousser
2. **Messages de commit clairs** : Utilisez des messages descriptifs pour faciliter le suivi des changements
3. **Branches de fonctionnalité** : Développez les nouvelles fonctionnalités sur des branches séparées
4. **Pull requests** : Utilisez des pull requests pour réviser le code avant de le fusionner avec main
5. **Surveillez les déploiements** : Vérifiez les logs sur Render après chaque déploiement

Modification et redéploiement
---------------------------

Pour apporter des modifications et les déployer :

1. Modifiez le code source
2. Committez et poussez les changements sur la branche main
3. GitHub Actions construira et publiera automatiquement une nouvelle image Docker
4. Render détectera la nouvelle image et la déploiera automatiquement

Le temps entre le push sur GitHub et le déploiement sur Render est généralement de quelques minutes. 