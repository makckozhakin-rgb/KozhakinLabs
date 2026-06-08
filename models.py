from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f'Комментарий от {self.author.username}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'