from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='Chris', password='password')

    def test_can_list_posts(self):
        Chris = User.objects.get(username='Chris')
        Post.objects.create(owner=Chris, title="a title")
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_posts(self):
        self.client.login(username='Chris', password='password')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_can_not_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        Chris = User.objects.create_user(username='Chris', password='password')
        Brian = User.objects.create_user(username='Brian', password='password')
        Post.objects.create(owner=Chris, title='a title', content='chriss content')
        Post.objects.create(owner=Brian, title='a new title', content='brians content')

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_fetch_post_by_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='Chris', password='password')
        response = self.client.get('/posts/1/', {'title': 'a title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_a_post_they_dont_own(self):
        self.client.login(username='Chris', password='password')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
