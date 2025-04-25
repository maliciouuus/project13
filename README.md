# Holiday Homes

![CI/CD Pipeline](https://github.com/maliciouuus/project13/actions/workflows/docker-build.yml)

Une application Django pour la gestion de locations de vacances et de profils utilisateurs.

## Présentation du projet

Holiday Homes est une application web développée avec Django qui permet aux utilisateurs de parcourir des annonces de locations de vacances et de consulter des profils d'utilisateurs. Ce projet a été conçu dans le cadre du parcours OpenClassrooms et démontre la mise en place d'une architecture CI/CD complète.

### Caractéristiques

- Architecture modulaire avec applications séparées (lettings, profiles)
- Section de locations pour parcourir les propriétés disponibles
- Section de profils pour consulter les informations des utilisateurs
- Interface d'administration pour gérer les données
- Intégration avec Sentry pour le suivi des erreurs
- Pipeline CI/CD complet avec GitHub Actions, Docker et Render
- Documentation technique complète avec Sphinx et Read the Docs

## Architecture du projet

Le projet a été réorganisé selon une architecture modulaire pour améliorer la maintenabilité et l'évolutivité:

- **oc_lettings_site**: Application principale contenant la configuration du projet
- **lettings**: Application dédiée à la gestion des locations et adresses
- **profiles**: Application dédiée à la gestion des profils utilisateurs

Cette séparation en applications distinctes permet:
- Une meilleure organisation du code
- Une séparation claire des responsabilités
- Un développement plus facile des nouvelles fonctionnalités
- Une maintenance simplifiée

## Installation et configuration

### Prérequis

- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)
- Docker (pour le développement avec conteneurs)
- Un compte Sentry (optionnel, pour le suivi des erreurs)

### Développement local

1. Cloner le dépôt:
   ```bash
   git clone https://github.com/maliciouuus/project13.git
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
   ALLOWED_HOSTS=.localhost,127.0.0.1,[::1],testserver
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

## Tests et qualité du code

### Exécution des tests

Le projet utilise pytest pour les tests:

```bash
# Exécuter tous les tests
pytest

# Exécuter les tests avec couverture de code
pytest --cov=.

# Vérifier que la couverture atteint au moins 80%
pytest --cov=. --cov-fail-under=80
```

### Linting et vérification du code

Pour vérifier la qualité du code:

```bash
# Exécuter flake8 pour vérifier le respect des normes PEP8
flake8
```

## Surveillance des erreurs avec Sentry

L'application est intégrée avec Sentry pour surveiller les erreurs en production:

1. Les erreurs et exceptions sont automatiquement capturées et envoyées à Sentry
2. La configuration de logging permet de capturer différents niveaux d'événements
3. Le décorateur `@log_function_call` est utilisé pour journaliser les appels de fonctions importantes

Pour tester l'intégration Sentry:
- Accédez à `/sentry-test/` (génère une exception délibérément)
- Vérifiez que l'erreur apparaît dans votre tableau de bord Sentry

## Pipeline CI/CD avec GitHub Actions

Ce projet utilise GitHub Actions pour l'intégration continue et la livraison continue avec déploiement automatique sur Render.

### Processus de la pipeline

La pipeline est divisée en deux étapes:

1. **Test et Linting**: 
   - Exécution automatique de flake8 pour vérifier la qualité du code
   - Exécution des tests pytest avec vérification de la couverture (minimum 80%)
   - Cette étape est exécutée pour toutes les branches et pull requests

2. **Build et Push Docker**: 
   - À chaque push sur la branche main, GitHub Actions construit automatiquement une image Docker
   - L'image est taguée avec `latest` et le hash du commit pour la traçabilité
   - L'image est publiée sur DockerHub avec le tag `purityoff/oc-lettings:latest`
   - Cette étape n'est exécutée que si les tests sont réussis

### Configuration des Secrets GitHub

Pour que la pipeline fonctionne correctement, configurez les secrets suivants dans votre dépôt GitHub (Settings > Secrets and variables > Actions):

| Secret | Description |
|--------|-------------|
| `DOCKER_USERNAME` | Nom d'utilisateur DockerHub (purityoff) |
| `DOCKER_PASSWORD` | Mot de passe ou token DockerHub |

### Configuration de Render

Pour configurer Render afin qu'il utilise l'image Docker:

1. Créez un nouveau service Web sur Render
2. Sélectionnez "Docker Registry" comme environnement
3. Entrez "purityoff/oc-lettings:nginx" comme Image URL
4. Configurez les variables d'environnement nécessaires (voir .env2)
5. Assurez-vous que le port est configuré sur 80 (et non 8000)

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
4. Pour déployer la nouvelle image sur Render:
   - Allez dans votre service sur Render
   - Cliquez sur "Manual Deploy" > "Deploy latest image"
   - Attendez que le déploiement se termine

### Extraire l'image depuis Docker Hub

Pour extraire l'image depuis Docker Hub et l'exécuter localement:

```bash
docker pull purityoff/oc-lettings:latest
docker run -p 8000:8000 --env-file .env purityoff/oc-lettings:latest
```

## Structure du projet

```
project13/
├── .github/workflows/       # Configuration GitHub Actions pour CI/CD
├── docs/                    # Documentation Sphinx
├── lettings/                # Application pour les locations
│   ├── migrations/          # Migrations de base de données
│   ├── templates/           # Templates spécifiques aux locations
│   ├── admin.py             # Configuration de l'admin pour les locations
│   ├── models.py            # Modèles Address et Letting
│   ├── urls.py              # URLs des locations
│   └── views.py             # Vues des locations
├── oc_lettings_site/        # Application principale
│   ├── management/          # Commandes personnalisées
│   ├── utils/               # Utilitaires (logging, etc.)
│   ├── settings.py          # Configuration du projet
│   └── urls.py              # URLs principales
├── profiles/                # Application pour les profils
│   ├── migrations/          # Migrations de base de données
│   ├── templates/           # Templates spécifiques aux profils
│   ├── admin.py             # Configuration de l'admin pour les profils
│   ├── models.py            # Modèle Profile
│   ├── urls.py              # URLs des profils
│   └── views.py             # Vues des profils
├── static/                  # Fichiers statiques (CSS, JS, images)
├── templates/               # Templates partagés
├── .coveragerc              # Configuration de coverage
├── .env.example             # Exemple de fichier .env
├── Dockerfile               # Configuration Docker
├── README.md                # Documentation principale
└── requirements.txt         # Dépendances Python
```

## Documentation technique

La documentation détaillée du projet est disponible sur Read the Docs:
- [Documentation complète](https://project13.readthedocs.io/en/latest/index.html)

Pour générer la documentation localement:
```bash
cd docs
pip install -r requirements.txt
make html
```

La documentation sera disponible dans `docs/_build/html/index.html`.

## Contributions

Les contributions à ce projet sont les bienvenues. Veuillez suivre ces étapes:

1. Forker le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Committer vos changements (`git commit -m 'Add some amazing feature'`)
4. Pousser la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.
