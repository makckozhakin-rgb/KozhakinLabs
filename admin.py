from django.contrib import admin
from .models import News, Comment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('author', 'published_date')
    search_fields = ('title', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'author', 'created_date', 'is_approved')
    list_filter = ('is_approved', 'created_date')