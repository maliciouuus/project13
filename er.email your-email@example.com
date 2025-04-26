[33mcommit cdb48bf11f439dc7eaf2021b0e33b7983a346ca7[m[33m ([m[1;36mHEAD -> [m[1;32mmain[m[33m, [m[1;31morigin/main[m[33m)[m
Author: VotreNouveauNom <votre.nouvel.email@example.com>
Date:   Fri Apr 25 20:24:17 2025 +0200

    Suppression des références au webhook Render dans le README

[1mdiff --git a/README.md b/README.md[m
[1mindex 837e2a4..700ddb3 100644[m
[1m--- a/README.md[m
[1m+++ b/README.md[m
[36m@@ -161,7 +161,7 @@[m [mCe projet utilise GitHub Actions pour l'intégration continue et la livraison co[m
 [m
 ### Processus de la pipeline[m
 [m
[31m-La pipeline est divisée en trois étapes:[m
[32m+[m[32mLa pipeline est divisée en deux étapes:[m
 [m
 1. **Test et Linting**: [m
    - Exécution automatique de flake8 pour vérifier la qualité du code[m
[36m@@ -174,11 +174,6 @@[m [mLa pipeline est divisée en trois étapes:[m
    - L'image est publiée sur DockerHub avec le tag `purityoff/oc-lettings:latest`[m
    - Cette étape n'est exécutée que si les tests sont réussis[m
 [m
[31m-3. **Déploiement sur Render**:[m
[31m-   - Après la construction de l'image, le hook de déploiement Render est déclenché[m
[31m-   - Render télécharge la nouvelle image Docker et la déploie[m
[31m-   - Cette étape n'est exécutée que si la construction de l'image est réussie[m
[31m-[m
 ### Configuration des Secrets GitHub[m
 [m
 Pour que la pipeline fonctionne correctement, configurez les secrets suivants dans votre dépôt GitHub (Settings > Secrets and variables > Actions):[m
[36m@@ -187,7 +182,6 @@[m [mPour que la pipeline fonctionne correctement, configurez les secrets suivants da[m
 |--------|-------------|[m
 | `DOCKER_USERNAME` | Nom d'utilisateur DockerHub (purityoff) |[m
 | `DOCKER_PASSWORD` | Mot de passe ou token DockerHub |[m
[31m-| `RENDER_DEPLOY_HOOK_URL` | URL du webhook de déploiement Render |[m
 [m
 ### Configuration de Render[m
 [m
[36m@@ -195,9 +189,9 @@[m [mPour configurer Render afin qu'il utilise l'image Docker:[m
 [m
 1. Créez un nouveau service Web sur Render[m
 2. Sélectionnez "Docker Registry" comme environnement[m
[31m-3. Entrez "purityoff/oc-lettings:latest" comme Image URL[m
[32m+[m[32m3. Entrez "purityoff/oc-lettings:nginx" comme Image URL[m
 4. Configurez les variables d'environnement nécessaires (voir .env2)[m
[31m-5. Activez le déploiement automatique lorsqu'une nouvelle image est publiée[m
[32m+[m[32m5. Assurez-vous que le port est configuré sur 80 (et non 8000)[m
 [m
 ### Application déployée[m
 [m
[36m@@ -216,8 +210,10 @@[m [mPour modifier et redéployer l'application:[m
    git push origin main[m
    ```[m
 3. GitHub Actions construira automatiquement une nouvelle image Docker[m
[31m-4. Render détectera la nouvelle image et la déploiera automatiquement[m
[31m-5. En quelques minutes, vos modifications seront visibles sur le site déployé[m
[32m+[m[32m4. Pour déployer la nouvelle image sur Render:[m
[32m+[m[32m   - Allez dans votre service sur Render[m
[32m+[m[32m   - Cliquez sur "Manual Deploy" > "Deploy latest image"[m
[32m+[m[32m   - Attendez que le déploiement se termine[m
 [m
 ### Extraire l'image depuis Docker Hub[m
 [m
