from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.contrib import messages
from .models import News, Comment
from .forms import CommentForm, NewsForm

def index(request):
    latest_news = News.objects.all()[:3]
    return render(request, 'newsapp/index.html', {'latest_news': latest_news})

def contacts(request):
    return render(request, 'newsapp/contacts.html')

def news_list(request):
    news = News.objects.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        news = news.filter(title__icontains=search_query)
    
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'oldest':
        news = news.order_by('published_date')
    else:
        news = news.order_by('-published_date')
    
    return render(request, 'newsapp/news_list.html', {
        'news': news,
        'search_query': search_query,
        'current_sort': sort_by
    })

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    comments = news_item.comments.filter(is_approved=True)
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news_item
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('news_detail', pk=pk)
    else:
        form = CommentForm()
    
    return render(request, 'newsapp/news_detail.html', {
        'news': news_item,
        'comments': comments,
        'form': form
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'newsapp/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'newsapp/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('index')

@login_required
def profile(request):
    user_comments = Comment.objects.filter(author=request.user)
    return render(request, 'newsapp/profile.html', {
        'user': request.user,
        'comments': user_comments
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменён!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'newsapp/change_password.html', {'form': form})

@staff_member_required
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Новость успешно добавлена!')
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm()
    return render(request, 'newsapp/add_news.html', {'form': form})

@staff_member_required
def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость успешно обновлена!')
            return redirect('news_detail', pk=pk)
    else:
        form = NewsForm(instance=news)
    return render(request, 'newsapp/edit_news.html', {'form': form, 'news': news})

@staff_member_required
def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Новость успешно удалена!')
        return redirect('news_list')
    return render(request, 'newsapp/delete_news.html', {'news': news})