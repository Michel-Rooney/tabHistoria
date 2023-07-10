from django.contrib import messages
from django.urls import resolve, reverse
from .. import views
from parameterized import parameterized
from .test_post_base import PostTestBase
from apps.post.models import Post, User


class PostViewsTest(PostTestBase):
    @parameterized.expand([
      ('post:post', {}, views.post),
      ('post:post_viewer', {'id': 1}, views.post_viewer),
      ('post:vote', {'id': 1}, views.vote),
      ('post:comment', {'id': 1}, views.comment),
      ('post:render_post', {'id': 1}, views.render_post),
      ('post:delete_post', {'pk_post': 1, 'pk_client': 1}, views.delete_post),
      ('post:update_post', {'pk_post': 1, 'pk_client': 1}, views.update_post),
    ])
    def test_post_view_function_is_correct(
        self, path_name, arguments, correct_view
    ):
        url = reverse(path_name, kwargs=arguments)
        view = resolve(url)
        self.assertIs(view.func, correct_view)

    @parameterized.expand([
      ('post:post', {}, 200),
      ('post:post_viewer', {'id': 1}, 200),
      ('post:vote', {'id': 1}, 200),
      ('post:comment', {'id': 1}, 302),
      ('post:render_post', {'id': 1}, 200),
      ('post:delete_post', {'pk_post': 1, 'pk_client': 2}, 302),
      ('post:update_post', {'pk_post': 1, 'pk_client': 2}, 302),
    ])
    def test_post_view_returns_status_code_expect(
        self, path_name, arguments, code
    ):
        client = self.make_login_client()
        user = User.objects.create_user(
            username='Post view', password='123')
        Post.objects.create(
            title='Title',
            creator=user,
            content='Content'
        )
        url = reverse(path_name, kwargs=arguments)
        response = client.get(url)
        self.assertEqual(response.status_code, code)

    @parameterized.expand([
        ('post:post_viewer', {'id': 1}, 'pages/post_viewer.html'),
        ('post:render_post', {'id': 1}, 'partials/render_post.html'),
        (
            'post:update_post',
            {'pk_post': 1, 'pk_client': 1},
            'pages/update_post.html'
        )
    ])
    def test_post_view_loads_correct_template(
        self, path_name, arguments, correct_template
    ):
        client = self.make_login_client()
        user = User.objects.first()
        Post.objects.create(
            title='Title',
            creator=user,
            content='Content'
        )
        url = reverse(path_name, kwargs=arguments)
        response = client.get(url)
        self.assertTemplateUsed(response, correct_template)

    @parameterized.expand([
      ('post:post', {}),
      ('post:post_viewer', {'id': 1}),
      ('post:vote', {'id': 1}),
      ('post:comment', {'id': 1}),
      ('post:render_post', {'id': 1}),
      ('post:delete_post', {'pk_post': 1, 'pk_client': 2}),
      ('post:update_post', {'pk_post': 1, 'pk_client': 2}),
    ])
    def test_post_invalid_request(self, path_name, arguments):
        client = self.make_login_client()
        url = reverse(path_name, kwargs=arguments)
        response = client.put(url)
        message = response.content.decode('utf-8')
        self.assertEqual(message, "Invalid request")

    def test_post_login_email_validation_error(self):
        client = self.make_login_client()
        data = {
            'title': '',
            'text_content': ''
            }
        url = reverse('post:post')
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Preencha todos os campos necessários.')
        self.assertEqual(response.url, '/post/')

    def test_post_create_is_success(self):
        client = self.make_login_client()
        data = {
            'title': 'Title',
            'text-content': 'Content'
        }
        url = reverse('post:post')
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Post criado com sucesso')
        self.assertEqual(response.url, '/client/profile/1/')

    def test_post_delete_is_success(self):
        client = self.make_login_client(
            username='Client delete',
            email='clientdelete@gmail.com'
        )
        self.make_post()
        url = reverse('post:delete_post', kwargs={
            'pk_post': 1, 'pk_client': 1
        })
        response = client.get(url)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Post excluído com sucesso.')
        self.assertEqual(response.url, '/client/profile/1/')

    def test_post_update_is_success(self):
        client = self.make_login_client(
            username='Client update',
            email='clientupdate@gmail.com'
        )
        self.make_post()
        url = reverse('post:update_post', kwargs={
            'pk_post': 1, 'pk_client': 1
        })
        data = {
            'title': 'New title update',
            'text-content': 'New content update'
        }
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Post atualizado com sucesso.')
        self.assertEqual(response.url, '/client/profile/1')

    def test_post_update_validation_error(self):
        client = self.make_login_client(
            username='Client update',
            email='clientupdate@gmail.com'
        )

        self.make_post()
        url = reverse('post:update_post', kwargs={
            'pk_post': 1, 'pk_client': 1
        })
        data = {
            'title': '',
            'text-content': ''
        }
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Preencha todos os campos necessários.')
        self.assertEqual(response.url, '/update_post/1/1/')

    def test_post_comment_vote_up_is_success(self):
        self.make_comment()
        client = self.make_login_client(
            username='vote',
            email='vote@gmail.com'
        )
        data = {
            'vote': 'up',
            'type': 'comment',
            'id-post': 1
        }
        url = reverse('post:vote', kwargs={'id': 1})
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Like realizado com sucesso.')
        self.assertEqual(response.url, '/post/1/')

    def test_post_comment_vote_down_is_success(self):
        self.make_comment()
        client = self.make_login_client(
            username='vote',
            email='vote@gmail.com'
        )
        data = {
            'vote': 'down',
            'type': 'comment',
            'id-post': 1
        }
        url = reverse('post:vote', kwargs={'id': 1})
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Deslike realizado com sucesso.')
        self.assertEqual(response.url, '/post/1/')

    def test_post_vote_up_is_success(self):
        self.make_post()
        client = self.make_login_client(
            username='vote',
            email='vote@gmail.com'
        )
        data = {
            'vote': 'up',
            'type': 'post',
            'id-post': 1
        }
        url = reverse('post:vote', kwargs={'id': 1})
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Like realizado com sucesso.')
        self.assertEqual(response.url, '/post/1/')

    def test_post_vote_down_is_success(self):
        self.make_post()
        client = self.make_login_client(
            username='vote',
            email='vote@gmail.com'
        )
        data = {
            'vote': 'down',
            'type': 'post',
            'id-post': 1
        }
        url = reverse('post:vote', kwargs={'id': 1})
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Deslike realizado com sucesso.')
        self.assertEqual(response.url, '/post/1/')

    def test_post_comment_comment_is_success(self):
        self.make_comment()
        client = self.make_login_client(
            username='comment',
            email='comment@gmail.com'
        )
        data = {
            'text-content': 'text content',
            'type': 'comment',
            'id-post': 1
        }
        url = reverse('post:comment', kwargs={'id': 1})
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Comentario feito com sucesso.')
        self.assertEqual(response.url, '/post/1/')

    def test_post_comment_post_is_success(self):
        self.make_post()
        client = self.make_login_client(
            username='comment',
            email='comment@gmail.com'
        )
        data = {
            'text-content': 'text content',
            'type': 'post',
            'id-post': 1
        }
        url = reverse('post:comment', kwargs={'id': 1})
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Comentario feito com sucesso.')
        self.assertEqual(response.url, '/post/1/')

    def test_post_comment_validation_error(self):
        client = self.make_login_client(
            username='comment',
            email='comment@gmail.com'
        )
        data = {
            'text-content': '',
            'type': '',
            'id-post': 1
        }
        url = reverse('post:comment', kwargs={'id': 1})
        response = client.post(url, data=data)
        stored_messages = list(messages.get_messages(response.wsgi_request))
        message = stored_messages[0].message
        self.assertEqual(message, 'Campo de comentário vazio.')
        self.assertEqual(response.url, '/post/1/')
