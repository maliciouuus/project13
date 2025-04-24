from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import Http404
from unittest.mock import patch
from profiles.models import Profile
from profiles.views import profile


class ProfilesTest(TestCase):
    """Test case for the profiles application."""

    def setUp(self):
        """Set up test data for profiles."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="test_user",
            email="test@test.com",
            password="test_password",
        )
        self.profile = Profile.objects.create(
            user=self.user,
            favorite_city="Test City",
        )

    def test_profiles_index(self):
        """Test the index view for profiles."""
        url = reverse("profiles:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profiles")

    def test_profile_detail(self):
        """Test the profile detail view."""
        url = reverse("profiles:profile", kwargs={"username": self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.profile.favorite_city)

    @patch("profiles.views.get_object_or_404")
    def test_profile_detail_error(self, mock_get_object):
        """Test the profile detail view error handling."""
        mock_get_object.side_effect = Http404("Profile not found")

        # Appeler directement la vue en utilisant le RequestFactory
        request = self.factory.get("/")
        with self.assertRaises(Http404):
            profile(request, "nonexistent")

    @patch("profiles.views.log_error")
    def test_profile_exception_logging(self, mock_log_error):
        """Test that exceptions in the profile view are properly logged."""
        # Configuration du mock pour lever une exception
        with patch("profiles.views.get_object_or_404") as mock_get:
            mock_get.side_effect = Exception("Test exception")

            # Création d'une requête
            request = self.factory.get("/")

            # Vérification que l'exception est bien propagée
            with self.assertRaises(Exception):
                profile(request, "nonexistent")

            # Vérification que log_error a été appelé avec les bons arguments
            mock_log_error.assert_called_once()
            self.assertIn(
                "Error retrieving profile with username nonexistent",
                mock_log_error.call_args[0][0],
            )

    def test_profile_str(self):
        """Test the string representation of Profile."""
        self.assertEqual(str(self.profile), self.user.username)
