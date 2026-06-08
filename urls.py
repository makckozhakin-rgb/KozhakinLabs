from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contacts/', views.contacts, name='contacts'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('news/add/', views.add_news, name='add_news'),
    path('news/edit/<int:pk>/', views.edit_news, name='edit_news'),
    path('news/delete/<int:pk>/', views.delete_news, name='delete_news'),
]