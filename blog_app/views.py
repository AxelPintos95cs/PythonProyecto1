from django.shortcuts import render, redirect, get_object_or_404
from .forms import AuthorForm, CategoryForm, PostForm
from .models import Post
from blog_app.models import Post, Category, Author


def home(request):
    posts = Post.objects.all().order_by('-created_at')[:5]  
    return render(request, 'blog_app/home.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog_app/post_detail.html', {'post': post})

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
    query = request.GET.get('q', '')  
    category = request.GET.get('category', '')  
    author = request.GET.get('author', '') 
    
    
    posts = Post.objects.all()
    
    if query:
        posts = posts.filter(title__icontains=query)  
    if category:
        posts = posts.filter(category__name__icontains=category)  
    if author:
        posts = posts.filter(author__name__icontains=author)  

    categories = Category.objects.all()  
    authors = Author.objects.all() 

    return render(request, 'blog_app/search_results.html', {
        'posts': posts,
        'categories': categories,
        'authors': authors,
        'query': query,
        'category': category,
        'author': author,
    })

