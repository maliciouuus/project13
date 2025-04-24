Pipeline CI/CD
==========

Cette section détaille le pipeline d'intégration et de déploiement continus (CI/CD) implémenté pour le projet Holiday Homes.

Vue d'ensemble
-------------

Le pipeline CI/CD est implémenté avec GitHub Actions et permet d'automatiser les tests, la construction, la publication et le déploiement de l'application. Le workflow est défini dans le fichier ``.github/workflows/ci-cd.yml``.

.. image:: https://mermaid.ink/img/pako:eNqFlMtugzAQRX8FzYZKlXhkQUiaTdWqVas-NrSLeCyCRYwjY5M0CvDvNQ6kJSk4rDyeO_fO2DOQxDIkmeCCLHdmsSHaZk1LZQItE5nNxFpbkmtF0iQzVtoJ0hxUbkfwmZmsA3xIDFo78gVH1lpIimnGTFFlrXvGljEE_iSQkTNmtCVreVoZmT8ksV2RJ5YJ1XD_0PChqGTIwFd-GC1OA39GoouL-dV4KdZQWgk1pO1Fs0ASLcS6ITsXXqzlJYMu7H-k5OeC6T_hN8dwWQW-74fdYs4KKkE1O6RWQxKdcpRMZLWiG6XvZ9MtZCmTxbw_FeElqCeJPqB26Xzx_KJ5rD6PIfX1wJnw7RcaLlGf-NQLS3e7d9tpDzkJViFxCU6UhCRGlxhHE8dxlSRRSsL3gY-j8Wy6nE6_1hGYNMExONH7bDSdRV-fXh_4HfXqY0-CGzfOxVJhMiOhx0nIrjcn4T8VeTuZ?type=png
   :alt: Pipeline CI/CD Flow
   :align: center

Le pipeline est divisé en cinq jobs principaux :

1. **Test**
2. **Vérification de sécurité**
3. **Documentation**
4. **Construction et publication Docker**
5. **Déploiement**

Job 1: Test
----------

Ce job est exécuté à chaque push sur la branche master et pour chaque pull request. Il effectue les actions suivantes :

.. code-block:: yaml

   test:
     runs-on: ubuntu-latest
     
     steps:
     - uses: actions/checkout@v3
     
     - name: Set up Python 3.9
       uses: actions/setup-python@v4
       with:
         python-version: '3.9'
         
     - name: Install dependencies
       run: |
         python -m pip install --upgrade pip
         pip install -r requirements.txt
         
     - name: Run tests with coverage
       run: |
         python -m pytest
         
     - name: Lint with flake8
       run: |
         flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
         flake8 . --count --exit-zero --max-complexity=10 --statistics
         
     - name: Check code formatting with black
       run: |
         pip install black
         black . --check --exclude=venv/
         
     - name: Upload coverage report
       uses: codecov/codecov-action@v3
       with:
         file: ./coverage.xml
         fail_ci_if_error: false

Ce job assure que :
- Les tests unitaires passent
- La couverture du code atteint au moins 80%
- Le code respecte les conventions de style
- Le formatage du code est conforme aux standards

Job 2: Vérification de sécurité
------------------------------

Ce job analyse le code pour détecter les vulnérabilités potentielles :

.. code-block:: yaml

   security-check:
     runs-on: ubuntu-latest
     needs: test
     
     steps:
     - uses: actions/checkout@v3
     
     - name: Set up Python 3.9
       uses: actions/setup-python@v4
       with:
         python-version: '3.9'
         
     - name: Install dependencies
       run: |
         python -m pip install --upgrade pip
         pip install bandit safety
         
     - name: Check security with bandit
       run: |
         bandit -r . -x ./venv,./docs,./tests
         
     - name: Check dependencies with safety
       run: |
         safety check -r requirements.txt

Ce job utilise deux outils de sécurité :
- **Bandit** : Analyse statique du code Python pour identifier les problèmes de sécurité
- **Safety** : Vérification des dépendances pour identifier les vulnérabilités connues

Job 3: Documentation
------------------

Ce job génère la documentation du projet :

.. code-block:: yaml

   docs:
     needs: test
     runs-on: ubuntu-latest
     
     steps:
     - uses: actions/checkout@v3
     
     - name: Set up Python 3.9
       uses: actions/setup-python@v4
       with:
         python-version: '3.9'
         
     - name: Install dependencies
       run: |
         python -m pip install --upgrade pip
         pip install -r requirements.txt
         
     - name: Build documentation
       run: |
         mkdir -p docs/_static
         cd docs && make html
         
     - name: Upload documentation
       uses: actions/upload-artifact@v3
       with:
         name: documentation
         path: docs/_build/html/

La documentation générée est sauvegardée comme artefact de build et peut être téléchargée depuis l'interface GitHub Actions.

Job 4: Construction et publication Docker
---------------------------------------

Ce job construit et publie l'image Docker sur DockerHub :

.. code-block:: yaml

   build-and-push:
     needs: [test, security-check, docs]
     if: github.ref == 'refs/heads/master' && github.event_name == 'push'
     runs-on: ubuntu-latest
     
     steps:
     - uses: actions/checkout@v3
     
     - name: Set up Docker Buildx
       uses: docker/setup-buildx-action@v2
       
     - name: Login to DockerHub
       uses: docker/login-action@v2
       with:
         username: ${{ secrets.DOCKERHUB_USERNAME }}
         password: ${{ secrets.DOCKERHUB_TOKEN }}
         
     - name: Extract metadata for Docker
       id: meta
       uses: docker/metadata-action@v4
       with:
         images: ${{ secrets.DOCKERHUB_USERNAME }}/project13
         
     - name: Build and push Docker image
       uses: docker/build-push-action@v4
       with:
         context: .
         push: true
         tags: |
           ${{ secrets.DOCKERHUB_USERNAME }}/project13:latest
           ${{ secrets.DOCKERHUB_USERNAME }}/project13:${{ github.sha }}
         cache-from: type=gha
         cache-to: type=gha,mode=max

Ce job utilise plusieurs actions GitHub :
- **docker/setup-buildx-action** : Configurer Buildx pour des builds plus efficaces
- **docker/login-action** : Authentification sur DockerHub
- **docker/metadata-action** : Extraction des métadonnées pour le tagging
- **docker/build-push-action** : Construction et publication de l'image

L'image est taguée avec :
- ``latest`` pour toujours pointer vers la dernière version
- Le SHA du commit pour assurer la traçabilité

Job 5: Déploiement
----------------

Ce job déploie l'application sur Render :

.. code-block:: yaml

   deploy:
     needs: build-and-push
     if: github.ref == 'refs/heads/master' && github.event_name == 'push'
     runs-on: ubuntu-latest
     steps:
     - name: Deploy to Render
       run: |
         curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK_URL }}

Le déploiement utilise un webhook Render qui déclenche un déploiement automatique.

Job 6: Validation du déploiement
------------------------------

Ce dernier job vérifie que le déploiement s'est correctement terminé :

.. code-block:: yaml

   validate-deployment:
     needs: deploy
     if: github.ref == 'refs/heads/master' && github.event_name == 'push'
     runs-on: ubuntu-latest
     steps:
     - name: Wait for deployment to complete
       run: sleep 60
       
     - name: Validate deployment
       run: |
         status_code=$(curl -s -o /dev/null -w "%{http_code}" ${{ secrets.DEPLOYMENT_URL }})
         if [ $status_code -ne 200 ]; then
           echo "Deployment validation failed with status code: $status_code"
           exit 1
         fi
         echo "Deployment validated successfully!"

Ce job :
- Attend que le déploiement soit terminé (pause de 60 secondes)
- Vérifie que le site répond avec un code HTTP 200

Configuration requise
-------------------

Pour que le pipeline fonctionne correctement, les secrets suivants doivent être configurés dans les paramètres du dépôt GitHub :

- ``DOCKERHUB_USERNAME`` : Nom d'utilisateur DockerHub
- ``DOCKERHUB_TOKEN`` : Token d'accès DockerHub
- ``RENDER_DEPLOY_HOOK_URL`` : URL du webhook de déploiement Render
- ``DEPLOYMENT_URL`` : URL de l'application déployée

Fonctionnement des branches
-------------------------

Le pipeline applique différentes règles selon le type d'événement :

- **Pull requests vers master** : Exécute uniquement les jobs de test, vérification de sécurité et documentation
- **Push sur master** : Exécute tous les jobs, y compris la construction, la publication et le déploiement

Cette configuration permet de valider les changements avant leur fusion dans la branche principale. 