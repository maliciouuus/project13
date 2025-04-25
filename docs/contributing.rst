Guide de contribution
=====================

Ce guide explique comment contribuer au projet Holiday Homes.

Prérequis
---------

Avant de commencer à contribuer, assurez-vous d'avoir :

- Python 3.9 ou supérieur
- Git
- Un environnement virtuel Python
- Un compte GitHub

Configuration de l'environnement de développement
------------------------------------------------

1. Clonez le dépôt :

.. code-block:: bash

   git clone https://github.com/maliciouuus/project13.git
   cd project13

2. Créez et activez un environnement virtuel :

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # sous Windows : venv\Scripts\activate

3. Installez les dépendances de développement :

.. code-block:: bash

   pip install -r requirements.txt

Processus de contribution
------------------------

1. Créez une branche pour votre fonctionnalité ou correction :

.. code-block:: bash

   git checkout -b feature/nom-de-votre-fonctionnalite

2. Effectuez vos modifications en suivant les standards de code.

3. Exécutez les tests pour vous assurer que tout fonctionne :

.. code-block:: bash

   python -m pytest

4. Vérifiez la qualité du code avec flake8 et black :

.. code-block:: bash

   flake8 .
   black --check .

5. Ajoutez vos modifications et créez un commit :

.. code-block:: bash

   git add .
   git commit -m "Description claire de vos changements"

6. Poussez votre branche vers GitHub :

.. code-block:: bash

   git push origin feature/nom-de-votre-fonctionnalite

7. Créez une Pull Request sur GitHub.

Standards de code
---------------

Le projet utilise plusieurs outils pour maintenir une qualité de code élevée :

- **Black** : Pour le formatage du code
- **Flake8** : Pour le linting et l'analyse statique
- **pytest** : Pour les tests unitaires

Veuillez vous assurer que votre code respecte ces standards avant de soumettre une Pull Request.

Documentation
------------

Si vous ajoutez de nouvelles fonctionnalités ou modifiez le comportement existant, assurez-vous de mettre à jour la documentation :

1. Mettez à jour ou ajoutez des docstrings à vos fonctions et classes
2. Mettez à jour les fichiers RST dans le répertoire `docs/`
3. Générez la documentation pour vérifier qu'elle s'affiche correctement :

.. code-block:: bash

   cd docs
   make html

Tests
-----

Toute nouvelle fonctionnalité doit être accompagnée de tests appropriés. Les tests doivent :

- Être placés dans le fichier de tests correspondant à l'application modifiée
- Utiliser l'infrastructure de test de Django (`TestCase`)
- Avoir un nom descriptif commençant par `test_`
- Inclure des assertions qui vérifient le comportement attendu

Structure du projet
-----------------

Avant de contribuer, familiarisez-vous avec la structure du projet :

- `lettings/` : Application pour la gestion des locations
- `profiles/` : Application pour la gestion des profils utilisateurs
- `oc_lettings_site/` : Configuration principale du projet Django
- `templates/` : Templates HTML
- `static/` : Fichiers statiques
- `docs/` : Documentation
- `.github/workflows/` : Configuration CI/CD

Signalement de bugs
-----------------

Si vous trouvez un bug, veuillez créer une issue sur GitHub avec :

- Une description claire du problème
- Les étapes pour reproduire le bug
- Les comportements attendu et observé
- Des captures d'écran si applicable

Contact
-------

Si vous avez des questions sur le processus de contribution, n'hésitez pas à contacter les mainteneurs du projet via GitHub. 