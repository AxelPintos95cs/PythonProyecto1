from django import forms
from .models import Author, Category, Post

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

