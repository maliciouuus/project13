Installation
============

Prérequis
--------

* Python 3.9 ou supérieur
* pip (gestionnaire de paquets Python)
* Git

Installation locale
-----------------

1. Cloner le dépôt :

.. code-block:: bash

   git clone https://github.com/maliciouuus/project13.git
   cd project13

2. Créer et activer un environnement virtuel :

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # Sous Windows : venv\Scripts\activate

3. Installer les dépendances :

.. code-block:: bash

   pip install -r requirements.txt

4. Copier le fichier de configuration :

.. code-block:: bash

   cp .env.example .env

5. Lancer les migrations :

.. code-block:: bash

   python manage.py migrate

6. Démarrer le serveur :

.. code-block:: bash

   python manage.py runserver

Le site est accessible à l'adresse http://127.0.0.1:8000/

Connexion à l'administration
---------------------------

Un utilisateur admin est créé automatiquement:

* **Nom d'utilisateur:** francis
* **Mot de passe:** francis

Utilisation avec Docker
---------------------

Construction et lancement:

.. code-block:: bash

   docker build -t oc-lettings:local .
   docker run -p 8000:8000 --env-file .env oc-lettings:local

Variables d'environnement
-----------------------

Les principales variables d'environnement:

* ``DEBUG`` : Mode débogage (True/False)
* ``SECRET_KEY`` : Clé secrète Django
* ``SENTRY_DSN`` : URL de connexion à Sentry

Diagramme de l'architecture
--------------------------

.. mermaid::

   graph TD
       A[Client] --> B[Django Application]
       B --> C[Lettings App]
       B --> D[Profiles App]
       C --> E[Database]
       D --> E
       B --> F[Sentry]
       
Dépannage
--------

En cas de problème, vérifiez:
* Les migrations sont bien appliquées
* L'environnement virtuel est activé
* Les variables d'environnement sont correctes 