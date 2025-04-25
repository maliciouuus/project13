# Holiday Homes

![CI/CD Pipeline](https://github.com/username/project13/actions/workflows/docker-build.yml/badge.svg)

Une application Django pour la gestion de locations de vacances et de profils utilisateurs.

## Présentation du projet

Holiday Homes est une application web développée avec Django qui permet aux utilisateurs de parcourir des annonces de locations de vacances et de consulter des profils d'utilisateurs. Ce projet a été conçu dans le cadre du parcours OpenClassrooms et démontre la mise en place d'une architecture CI/CD complète.

### Caractéristiques

- Section de locations pour parcourir les propriétés disponibles
- Section de profils pour consulter les informations des utilisateurs
- Interface d'administration pour gérer les données
- Intégration avec Sentry pour le suivi des erreurs
- Pipeline CI/CD avec GitHub Actions

## Installation et configuration

### Développement local

1. Cloner le dépôt:
   ```bash
   git clone https://github.com/yourusername/project13.git
   cd project13
   ```

2. Créer et activer un environnement virtuel:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sous Windows: venv\Scripts\activate
   ```

3. Installer les dépendances:
   ```bash
   pip install -r requirements.txt
   ```

4. Créer un fichier `.env` basé sur `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Puis mettre à jour les valeurs dans le fichier `.env` avec vos propres paramètres:
   ```
   # Variables d'environnement requises
   DJANGO_SECRET_KEY=votre_cle_secrete
   DEBUG=True
   ALLOWED_HOSTS=.localhost,127.0.0.1,[::1]
   SENTRY_DSN=votre_dsn_sentry  # Laisser vide pour désactiver Sentry
   ```

5. Exécuter les migrations:
   ```bash
   python manage.py migrate
   ```

6. Créer un superutilisateur:
   ```bash
   python manage.py create_superuser
   ```

7. Démarrer le serveur de développement:
   ```bash
   python manage.py runserver
   ```

L'application sera accessible à l'adresse http://localhost:8000/

### Test Docker en local

Pour tester l'application avec Docker en local:

1. Construire l'image Docker:
   ```bash
   docker build -t holiday-homes:local .
   ```

2. Lancer le conteneur:
   ```bash
   docker run -p 8000:8000 --env-file .env holiday-homes:local
   ```

Si le port 8000 est déjà utilisé, vous pouvez en utiliser un autre:
   ```bash
   docker run -p 9090:8000 --env-file .env holiday-homes:local
   ```

Un superutilisateur est automatiquement créé au premier démarrage avec les identifiants suivants:
- **Nom d'utilisateur:** francis
- **Mot de passe:** francis

Vous pouvez l'utiliser pour accéder à l'interface d'administration à l'adresse http://localhost:8000/admin/.

L'application sera accessible à l'adresse http://localhost:8000/ ou http://localhost:9090/ (selon le port choisi).

## Tests

Exécuter les tests avec pytest:

```bash
pytest
```

## Pipeline CI/CD avec GitHub Actions

Ce projet utilise GitHub Actions pour l'intégration continue et la livraison continue avec déploiement automatique sur Render.

### Processus de la pipeline

La pipeline est simple et efficace:

1. **Build et Push Docker**: 
   - À chaque push sur la branche main, GitHub Actions construit automatiquement une image Docker
   - L'image est ensuite publiée sur DockerHub avec le tag `purityoff/oc-lettings:latest`
   - Cette étape utilise le fichier `Dockerfile` à la racine du projet

2. **Déploiement automatique sur Render**:
   - Render est configuré pour surveiller cette image Docker
   - Dès qu'une nouvelle version de l'image est publiée, Render la détecte automatiquement
   - Render télécharge et déploie la nouvelle image sans intervention manuelle

Ce workflow simplifié permet:
- Un processus de déploiement rapide et fiable
- Une traçabilité complète (chaque version déployée correspond à une image Docker)
- Une séparation claire entre la construction (GitHub Actions) et le déploiement (Render)

### Configuration des Secrets GitHub

Pour que la pipeline fonctionne correctement, vous devez configurer les secrets suivants dans votre dépôt GitHub (Settings > Secrets and variables > Actions):

| Secret | Description |
|--------|-------------|
| `DOCKER_USERNAME` | Nom d'utilisateur DockerHub (purityoff) |
| `DOCKER_PASSWORD` | Mot de passe ou token DockerHub |

### Application déployée

L'application est déployée et accessible à l'URL suivante:
- [https://project13-r64u.onrender.com](https://project13-r64u.onrender.com)

### Modification et redéploiement

Pour modifier et redéployer l'application:

1. Effectuez vos modifications dans le code (par exemple, changer le titre dans index.html)
2. Committez et poussez les modifications sur la branche main:
   ```bash
   git add .
   git commit -m "Update title in index.html"
   git push origin main
   ```
3. GitHub Actions construira automatiquement une nouvelle image Docker
4. Render détectera la nouvelle image et la déploiera automatiquement
5. En quelques minutes, vos modifications seront visibles sur le site déployé

### Extraire l'image depuis Docker Hub

Pour extraire l'image depuis Docker Hub et l'exécuter localement:

```bash
docker pull purityoff/oc-lettings:latest
docker run -p 8000:8000 --env-file .env purityoff/oc-lettings:latest
```

## Structure du projet

- `lettings/`: Application pour la gestion des locations
- `profiles/`: Application pour la gestion des profils utilisateurs
- `oc_lettings_site/`: Configuration principale du projet Django
- `templates/`: Templates HTML
- `static/`: Fichiers statiques (CSS, JS, images)
- `.github/workflows/`: Configuration de GitHub Actions pour le CI/CD

## Contributions

Les contributions à ce projet sont les bienvenues. Veuillez suivre ces étapes:

1. Forker le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Committer vos changements (`git commit -m 'Add some amazing feature'`)
4. Pousser la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.
