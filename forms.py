from django import forms
from .models import Comment, News

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишите ваш комментарий...'})
        }
        labels = {
            'text': 'Ваш комментарий'
        }

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Содержание...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }