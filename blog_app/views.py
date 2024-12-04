from django.shortcuts import render, redirect
from .forms import AuthorForm, CategoryForm, PostForm
from .models import Post

def home(request):
    return render(request, 'blog_app/home.html')

def about(request):
    return render(request, 'blog_app/about.html')

def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AuthorForm()
    return render(request, 'blog_app/create_author.html', {'form': form})

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'blog_app/create_category.html', {'form': form})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog_app/create_post.html', {'form': form})

def search_posts(request):
    query = request.GET.get('q')
    results = Post.objects.filter(title__icontains=query) if query else None
    return render(request, 'blog_app/search_posts.html', {'results': results, 'query': query})

