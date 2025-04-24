Installation
============

Cette section explique comment installer et configurer le projet Holiday Homes pour le développement et le déploiement.

Prérequis
--------

* Python 3.9 ou supérieur
* pip (gestionnaire de paquets Python)
* Git
* Docker (optionnel, pour la conteneurisation)

Configuration pour le développement local
----------------------------------------

1. Cloner le dépôt :

.. code-block:: bash

   git clone https://github.com/yourusername/project13.git
   cd project13

2. Créer et activer un environnement virtuel :

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # Sous Windows : venv\Scripts\activate

3. Installer les dépendances :

.. code-block:: bash

   pip install -r requirements.txt

4. Créer un fichier `.env` basé sur `.env.example` :

.. code-block:: bash

   cp .env.example .env

5. Éditer le fichier `.env` avec vos propres valeurs de configuration.

6. Exécuter les migrations pour créer la structure de la base de données :

.. code-block:: bash

   python manage.py migrate

7. Créer un superutilisateur pour accéder à l'interface d'administration :

.. code-block:: bash

   python manage.py createsuperuser

8. Lancer le serveur de développement :

.. code-block:: bash

   python manage.py runserver

Le site devrait maintenant être accessible à l'adresse http://127.0.0.1:8000/.

Configuration avec Docker
-----------------------

1. Construire et lancer l'application avec Docker Compose :

.. code-block:: bash

   docker-compose up

2. Pour exécuter uniquement les tests :

.. code-block:: bash

   docker-compose run tests

3. Pour arrêter tous les services :

.. code-block:: bash

   docker-compose down

4. Pour construire l'image sans lancer les services :

.. code-block:: bash

   docker-compose build

Variables d'environnement
-----------------------

Le projet utilise des variables d'environnement pour configurer divers aspects de l'application. Les principales variables sont :

* ``DEBUG`` : Active/désactive le mode débogage (``True`` ou ``False``)
* ``SECRET_KEY`` : Clé secrète utilisée par Django pour les opérations cryptographiques
* ``SENTRY_DSN`` : URL de connexion à Sentry pour le suivi des erreurs
* ``SENTRY_ENVIRONMENT`` : Environnement Sentry (``development``, ``production``, etc.)
* ``SENTRY_TRACES_SAMPLE_RATE`` : Taux d'échantillonnage pour les traces Sentry (entre 0.0 et 1.0)
* ``RENDER`` : Indique si l'application s'exécute sur Render (``True`` ou ``False``)
* ``DATABASE_URL`` : URL de connexion à la base de données (pour PostgreSQL en production)

Configuration des services externes
--------------------------------

### Sentry

1. Créez un compte sur [Sentry](https://sentry.io)
2. Créez un nouveau projet Django
3. Copiez le DSN dans votre fichier `.env`

### DockerHub

1. Créez un compte sur [DockerHub](https://hub.docker.com)
2. Créez un nouveau dépôt pour stocker vos images
3. Générez un token d'accès dans les paramètres de votre compte

### Render

1. Créez un compte sur [Render](https://render.com)
2. Créez un nouveau service Web
3. Connectez-le à votre dépôt GitHub
4. Configurez les variables d'environnement requises

Dépannage
--------

**Erreur de migration** : Si vous rencontrez des erreurs lors des migrations, essayez :

.. code-block:: bash

   python manage.py migrate --run-syncdb

**Erreur de module introuvable** : Vérifiez que vous êtes bien dans l'environnement virtuel et que toutes les dépendances sont installées.

**Erreur de connexion à Sentry** : Vérifiez que votre DSN Sentry est correct et que votre réseau permet la connexion à Sentry.

**Erreur avec Docker** : Assurez-vous que Docker Desktop est en cours d'exécution et que le fichier `Dockerfile` est à la racine du projet. 