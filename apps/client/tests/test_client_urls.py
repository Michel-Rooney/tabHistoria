from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class ClientURLsTest(TestCase):
    @parameterized.expand([
        ('client:profile', '/client/profile/1/'),
        ('client:update_profile', '/client/update_profile/1/')
    ])
    def test_client_url_is_correct(self, path_name, correct_url):
        url = reverse(path_name, kwargs={'id': 1})
        self.assertEqual(url, correct_url)
