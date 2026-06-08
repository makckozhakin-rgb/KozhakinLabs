from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import News, Comment

class ModelTests(TestCase):
    def test_create_news(self):
        """Тест 1: Создание новости"""
        user = User.objects.create_user(username='testuser', password='12345')
        news = News.objects.create(
            title='Test News',
            content='Test Content',
            author=user,
            published_date=timezone.now()
        )
        self.assertEqual(news.title, 'Test News')
        self.assertEqual(str(news), 'Test News')

    def test_create_comment(self):
        """Тест 2: Создание комментария"""
        user = User.objects.create_user(username='testuser', password='12345')
        news = News.objects.create(
            title='Test News',
            content='Test Content',
            author=user
        )
        comment = Comment.objects.create(
            news=news,
            author=user,
            text='Test Comment',
            is_approved=True
        )
        self.assertEqual(comment.text, 'Test Comment')
        self.assertTrue(comment.is_approved)

    def test_news_string_representation(self):
        """Тест 3: Строковое представление новости"""
        user = User.objects.create_user(username='testuser', password='12345')
        news = News.objects.create(
            title='My News Title',
            content='Content',
            author=user
        )
        self.assertEqual(str(news), 'My News Title')

    def test_comment_string_representation(self):
        """Тест 4: Строковое представление комментария"""
        user = User.objects.create_user(username='testuser', password='12345')
        news = News.objects.create(
            title='Test News',
            content='Content',
            author=user
        )
        comment = Comment.objects.create(
            news=news,
            author=user,
            text='Hello',
            is_approved=True
        )
        self.assertIn('testuser', str(comment))


class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.news = News.objects.create(
            title='Тестовая новость',
            content='Содержание',
            author=self.user,
            published_date=timezone.now()
        )

    def test_home_page_status_code(self):
        """Тест 5: Главная страница доступна (200 OK)"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_news_list_page_status_code(self):
        """Тест 6: Страница новостей доступна (200 OK)"""
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)

    def test_news_detail_page_status_code(self):
        """Тест 7: Страница отдельной новости доступна (200 OK)"""
        response = self.client.get(reverse('news_detail', args=[self.news.id]))
        self.assertEqual(response.status_code, 200)

    def test_contacts_page_status_code(self):
        """Тест 8: Страница контактов доступна (200 OK)"""
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)