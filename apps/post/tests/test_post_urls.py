from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class PostURLsTest(TestCase):
    @parameterized.expand([
      ('post:post', {}, '/post/'),
      ('post:post_viewer', {'id': 1}, '/post/1/'),
      ('post:vote', {'id': 1}, '/vote/1/'),
      ('post:comment', {'id': 1}, '/comment/1/'),
      ('post:render_post', {'id': 1}, '/render_post/1/'),
      ('post:delete_post', {'pk_post': 1, 'pk_client': 1}, '/delete_post/1/1/'),
      ('post:update_post', {'pk_post': 1, 'pk_client': 1}, '/update_post/1/1/'),
    ])
    def test_post_url_is_correct(self, path_name, arguments, correct_url):
        url = reverse(path_name, kwargs=arguments)
        self.assertEqual(url, correct_url)
