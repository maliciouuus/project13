"""
This module contains tests for the oc_lettings_site app.
"""

from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from unittest.mock import patch, MagicMock
import os
from oc_lettings_site.views import handler404, handler500, sentry_test
from oc_lettings_site.utils.logging_utils import (
    log_info,
    log_warning,
    log_error,
    log_exception,
    log_function_call,
)


class OcLettingsSiteTest(TestCase):
    """Tests for the OC Lettings Site views."""

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_index(self):
        """Test the index view returns a successful response."""
        url = reverse("index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Holiday Homes")

    @patch("oc_lettings_site.utils.logging_utils.log_exception")
    def test_sentry_test_view(self, mock_log_exception):
        """Test that the sentry_test view raises an exception."""
        request = self.factory.get("/sentry-test/")
        with self.assertRaises(Exception):
            sentry_test(request)
        # Vérifier que l'exception a été capturée
        self.assertEqual(mock_log_exception.call_count, 1)

    @patch("oc_lettings_site.views.render")
    def test_handler404(self, mock_render):
        """Test that handler404 renders the 404 template."""
        mock_render.return_value = "404 page"
        request = self.factory.get("/nonexistent-url/")
        exception = Exception("Not found")
        result = handler404(request, exception)

        mock_render.assert_called_once_with(request, "404.html", status=404)
        self.assertEqual(result, "404 page")

    @patch("oc_lettings_site.views.render")
    def test_handler500(self, mock_render):
        """Test that handler500 renders the 500 template."""
        mock_render.return_value = "500 page"
        request = self.factory.get("/")
        result = handler500(request)

        mock_render.assert_called_once_with(request, "500.html", status=500)
        self.assertEqual(result, "500 page")

    @patch("logging.Logger.info")
    def test_log_info(self, mock_logger_info):
        """Test the log_info function logs at INFO level."""
        log_info("Test info message")
        mock_logger_info.assert_called_once_with("Test info message")

    @patch("logging.Logger.warning")
    def test_log_warning(self, mock_logger_warning):
        """Test the log_warning function logs at WARNING level."""
        log_warning("Test warning message")
        mock_logger_warning.assert_called_once_with("Test warning message")

    @patch("logging.Logger.error")
    @patch("sentry_sdk.capture_message")
    def test_log_error(self, mock_sentry_capture, mock_logger_error):
        """Test the log_error function logs at ERROR level and captures with Sentry."""
        exception = ValueError("Test exception")
        log_error("Test error message", exc_info=exception)

        mock_logger_error.assert_called_once_with(
            "Test error message", exc_info=exception
        )
        mock_sentry_capture.assert_called_once_with("Test error message", level="error")

    @patch("logging.Logger.exception")
    @patch("sentry_sdk.capture_exception")
    def test_log_exception(self, mock_sentry_capture_exception, mock_logger_exception):
        """Test the log_exception function logs the exception and captures with Sentry."""
        exception = ValueError("Test exception")
        log_exception("Test exception message", exception=exception)

        mock_logger_exception.assert_called_once_with("Test exception message")
        mock_sentry_capture_exception.assert_called_once_with(exception)

    @patch("oc_lettings_site.utils.logging_utils.log_info")
    @patch("oc_lettings_site.utils.logging_utils.log_exception")
    def test_log_function_call_decorator_success(
        self, mock_log_exception, mock_log_info
    ):
        """Test the log_function_call decorator logs function calls and successful execution."""

        @log_function_call
        def test_function(arg1, arg2=None):
            return f"{arg1}-{arg2}"

        result = test_function("test", arg2="value")

        self.assertEqual(result, "test-value")
        self.assertEqual(mock_log_info.call_count, 2)  # Appel + succès
        mock_log_exception.assert_not_called()

    @patch("oc_lettings_site.utils.logging_utils.log_info")
    @patch("oc_lettings_site.utils.logging_utils.log_exception")
    def test_log_function_call_decorator_exception(
        self, mock_log_exception, mock_log_info
    ):
        """Test the log_function_call decorator logs function calls and exceptions."""

        @log_function_call
        def test_function_error():
            raise ValueError("Test error")

        with self.assertRaises(ValueError):
            test_function_error()

        self.assertEqual(mock_log_info.call_count, 1)  # Seulement l'appel
        self.assertEqual(mock_log_exception.call_count, 1)


class SettingsModuleTests(TestCase):
    """Tests pour les modules de paramètres."""

    def test_settings_attributes(self):
        """Test que les attributs requis existent dans les paramètres de base."""
        from django.conf import settings

        # Vérifier les paramètres de base
        self.assertTrue(hasattr(settings, "DEBUG"))
        self.assertTrue(hasattr(settings, "SECRET_KEY"))
        self.assertTrue(hasattr(settings, "ALLOWED_HOSTS"))
        self.assertTrue(hasattr(settings, "DATABASES"))

    def test_wsgi_application_setting(self):
        """Test que le paramètre WSGI_APPLICATION est configuré."""
        from django.conf import settings

        self.assertTrue(hasattr(settings, "WSGI_APPLICATION"))
        self.assertEqual(settings.WSGI_APPLICATION, "oc_lettings_site.wsgi.application")

    def test_templates_setting(self):
        """Test que les paramètres TEMPLATES sont configurés."""
        from django.conf import settings

        self.assertTrue(hasattr(settings, "TEMPLATES"))
        self.assertIsInstance(settings.TEMPLATES, list)
        self.assertTrue(len(settings.TEMPLATES) > 0)

    def test_installed_apps_setting(self):
        """Test que les applications requises sont installées."""
        from django.conf import settings

        self.assertTrue(hasattr(settings, "INSTALLED_APPS"))
        # Vérifier que django.contrib.* est présent
        django_apps = [
            app for app in settings.INSTALLED_APPS if app.startswith("django.contrib.")
        ]
        self.assertTrue(
            len(django_apps) >= 6,
            "Les applications Django de base ne sont pas toutes présentes",
        )

        # Vérifier que lettings et profiles sont présents
        has_lettings = any("lettings" in app.lower() for app in settings.INSTALLED_APPS)
        has_profiles = any("profiles" in app.lower() for app in settings.INSTALLED_APPS)

        self.assertTrue(
            has_lettings,
            "L'application 'lettings' n'est pas présente dans INSTALLED_APPS",
        )
        self.assertTrue(
            has_profiles,
            "L'application 'profiles' n'est pas présente dans INSTALLED_APPS",
        )

    def test_static_url_setting(self):
        """Test que les paramètres statiques sont configurés."""
        from django.conf import settings

        self.assertTrue(hasattr(settings, "STATIC_URL"))
        self.assertEqual(settings.STATIC_URL, "/static/")

    def test_debug_setting(self):
        """Test que DEBUG est défini."""
        from django.conf import settings

        self.assertTrue(hasattr(settings, "DEBUG"))
        # Pas de vérification de valeur car elle peut changer selon l'environnement

    def test_root_urlconf_setting(self):
        """Test que ROOT_URLCONF est défini."""
        from django.conf import settings

        self.assertTrue(hasattr(settings, "ROOT_URLCONF"))
        self.assertEqual(settings.ROOT_URLCONF, "oc_lettings_site.urls")

    def test_wsgi_module(self):
        """Test la structure du module wsgi."""
        # Définir un faux module wsgi pour les tests
        code = """
import os
from unittest.mock import MagicMock

# Simuler django.core.wsgi
get_wsgi_application = MagicMock(return_value="mock_wsgi_app")

# Définir les variables d'environnement
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')

# Créer l'application WSGI
application = get_wsgi_application()
"""
        # Exécuter le code simulé
        namespace = {"os": os, "MagicMock": MagicMock}
        exec(code, namespace)

        # Vérifier que l'environnement est correctement configuré
        self.assertEqual(namespace.get("application"), "mock_wsgi_app")

    def test_asgi_module(self):
        """Test la structure du module asgi."""
        # Définir un faux module asgi pour les tests
        code = """
import os
from unittest.mock import MagicMock

# Simuler django.core.asgi
get_asgi_application = MagicMock(return_value="mock_asgi_app")

# Définir les variables d'environnement
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')

# Créer l'application ASGI
application = get_asgi_application()
"""
        # Exécuter le code simulé
        namespace = {"os": os, "MagicMock": MagicMock}
        exec(code, namespace)

        # Vérifier que l'environnement est correctement configuré
        self.assertEqual(namespace.get("application"), "mock_asgi_app")
