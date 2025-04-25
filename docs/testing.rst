Tests
=====

Types de tests
------------

Le projet utilise plusieurs types de tests:

* **Tests unitaires**: Tester les fonctions et méthodes individuelles
* **Tests d'intégration**: Tester l'interaction entre composants
* **Tests de vues**: Vérifier le bon fonctionnement des vues Django
* **Tests de modèles**: Vérifier les modèles de données
* **Linting**: Vérifier la qualité du code

Exécution des tests
-----------------

Pour exécuter tous les tests:

.. code-block:: bash

   pytest

Pour vérifier la couverture de code:

.. code-block:: bash

   pytest --cov=.

Pour exécuter le linting:

.. code-block:: bash

   flake8

Structure des tests
----------------

Les tests sont organisés par application:

* `lettings/tests.py`: Tests pour l'application lettings
* `profiles/tests.py`: Tests pour l'application profiles
* `oc_lettings_site/tests.py`: Tests pour l'application principale

Objectifs de qualité
------------------

* Couverture de code minimale: 80%
* Zéro erreur de linting
* Tests automatisés dans la pipeline CI/CD

Test manuel
---------

Tester manuellement les fonctionnalités principales:

1. Navigation sur la page d'accueil
2. Consultation de la liste des locations
3. Consultation des détails d'une location
4. Consultation de la liste des profils
5. Consultation des détails d'un profil
6. Test de l'intégration Sentry via `/sentry-test/`

Framework de tests
----------------

Le projet utilise pytest et les outils de test de Django pour implémenter les tests. Les tests sont organisés par application :

* `lettings/tests.py` : Tests pour l'application lettings
* `profiles/tests.py` : Tests pour l'application profiles
* `oc_lettings_site/tests.py` : Tests pour l'application principale

Exécution des tests
-----------------

Pour exécuter tous les tests :

.. code-block:: bash

   python -m pytest

Pour exécuter les tests avec rapport de couverture :

.. code-block:: bash

   python -m pytest --cov=. --cov-report=html
   # Ouvrez htmlcov/index.html pour visualiser le rapport de couverture

Pour exécuter les tests d'une application spécifique :

.. code-block:: bash

   python -m pytest lettings/
   python -m pytest profiles/
   python -m pytest oc_lettings_site/

Pour exécuter un test spécifique :

.. code-block:: bash

   python -m pytest lettings/tests.py::LettingTest::test_letting_list_view

Intégration continue
------------------

Les tests sont automatiquement exécutés dans le cadre du pipeline CI/CD défini dans `.github/workflows/ci-cd.yml`.
Le pipeline garantit que :

1. Tous les tests passent
2. La couverture du code est d'au moins 80%
3. Le code respecte les exigences de linting via flake8
4. Le code est correctement formaté via black

Configuration de la couverture
----------------------------

Le projet utilise `.coveragerc` pour configurer les paramètres de couverture des tests :

* Exigence minimale de couverture : 80%
* Chemins exclus : tests, migrations, settings, etc.
* Affichage des lignes manquantes dans les rapports de couverture

Écriture des tests
----------------

Le projet utilise les classes de test Django pour faciliter les tests d'intégration. Voici un exemple de test pour une vue de letting :

.. code-block:: python

   from django.test import TestCase
   from django.urls import reverse
   from .models import Address, Letting

   class LettingTest(TestCase):
       """Tests pour l'application Letting"""

       def setUp(self):
           """Préparer les données de test"""
           self.address = Address.objects.create(
               number=123,
               street="Test Street",
               city="Test City",
               state="TS",
               zip_code=12345,
               country_iso_code="TST",
           )

           self.letting = Letting.objects.create(
               title="Test Letting", address=self.address
           )

       def test_letting_list_view(self):
           """Tester la vue de liste des lettings"""
           url = reverse("lettings:index")
           response = self.client.get(url)
           self.assertEqual(response.status_code, 200)
           self.assertContains(response, "Lettings")

Lorsque vous écrivez des tests :

1. Placez les tests dans le fichier `tests.py` de l'application correspondante
2. Utilisez `TestCase` de Django comme classe de base
3. Configurez les données de test dans la méthode `setUp`
4. Nommez les méthodes de test avec un préfixe `test_`
5. Utilisez des assertions pour valider les résultats attendus
6. Documentez l'objectif de chaque fonction de test

Tests avec fixtures
----------------

Pour les tests qui nécessitent des données plus complexes, vous pouvez utiliser des fixtures :

1. Créez un répertoire `fixtures` dans votre application
2. Créez des fichiers JSON contenant les données de test
3. Chargez les fixtures dans vos tests :

.. code-block:: python

   class LettingFixtureTest(TestCase):
       fixtures = ['lettings.json', 'addresses.json']

       def test_with_fixtures(self):
           # Les données des fixtures sont chargées automatiquement
           letting = Letting.objects.get(pk=1)
           self.assertEqual(letting.title, "Attendu")

Tests de modèles
--------------

Les tests de modèles vérifient le comportement des modèles de données :

.. code-block:: python

   def test_address_str(self):
       """Tester la représentation en chaîne de caractères de l'adresse"""
       address = Address.objects.create(
           number=123,
           street="Test Street",
           city="Test City",
           state="TS",
           zip_code=12345,
           country_iso_code="TST",
       )
       self.assertEqual(str(address), "123 Test Street")

Tests de vues
-----------

Les tests de vues vérifient le comportement des vues Django :

.. code-block:: python

   def test_profile_detail_view(self):
       """Tester la vue de détail du profil"""
       url = reverse("profiles:profile", args=[self.user.username])
       response = self.client.get(url)
       self.assertEqual(response.status_code, 200)
       self.assertContains(response, self.user.username)

Mocking
------

Pour tester le code qui interagit avec des services externes (comme Sentry), utilisez le mocking :

.. code-block:: python

   from unittest.mock import patch

   @patch('sentry_sdk.capture_message')
   def test_error_logging(self, mock_capture_message):
       """Tester le logging d'erreur avec Sentry"""
       from oc_lettings_site.utils.logging_utils import log_error
       
       log_error("Test error")
       mock_capture_message.assert_called_once_with("Test error", level="error") 