from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.http import Http404
from unittest.mock import patch
from lettings.models import Address, Letting
from lettings.views import letting


class LettingsTest(TestCase):
    """Test case for the lettings application."""

    def setUp(self):
        """Set up test data for lettings."""
        self.factory = RequestFactory()
        self.address = Address.objects.create(
            number=1,
            street="Test Street",
            city="Test City",
            state="TS",
            zip_code=12345,
            country_iso_code="TST",
        )
        self.letting = Letting.objects.create(
            title="Test Letting",
            address=self.address,
        )

    def test_lettings_index(self):
        """Test the index view for lettings."""
        url = reverse("lettings:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lettings")

    def test_letting_detail(self):
        """Test the letting detail view."""
        url = reverse("lettings:letting", kwargs={"letting_id": self.letting.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.letting.title)
        self.assertContains(response, self.address.street)

    @patch("lettings.views.get_object_or_404")
    def test_letting_detail_error(self, mock_get_object):
        """Test the letting detail view error handling."""
        mock_get_object.side_effect = Http404("Letting not found")

        # Appeler directement la vue en utilisant le RequestFactory
        request = self.factory.get("/")
        with self.assertRaises(Http404):
            letting(request, 9999)

    @patch("lettings.views.log_error")
    def test_letting_exception_logging(self, mock_log_error):
        """Test that exceptions in the letting view are properly logged."""
        # Configuration du mock pour lever une exception
        with patch("lettings.views.get_object_or_404") as mock_get:
            mock_get.side_effect = Exception("Test exception")

            # Création d'une requête
            request = self.factory.get("/")

            # Vérification que l'exception est bien propagée
            with self.assertRaises(Exception):
                letting(request, 9999)

            # Vérification que log_error a été appelé avec les bons arguments
            mock_log_error.assert_called_once()
            self.assertIn(
                "Error retrieving letting with ID 9999", mock_log_error.call_args[0][0]
            )

    def test_address_str(self):
        """Test the string representation of Address."""
        expected = (
            f"{self.address.number} {self.address.street}, "
            f"{self.address.city}, {self.address.state} {self.address.zip_code}"
        )
        self.assertEqual(str(self.address), expected)

    def test_letting_str(self):
        """Test the string representation of Letting."""
        self.assertEqual(str(self.letting), self.letting.title)
