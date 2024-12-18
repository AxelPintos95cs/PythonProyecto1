from django.shortcuts import render, redirect, get_object_or_404
from .forms import AuthorForm, CategoryForm, PostForm
from .models import Post
from blog_app.models import Post, Category, Author
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count

def home(request):
    posts = Post.objects.all().order_by('-created_at')[:5]  
    return render(request, 'blog_app/home.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog_app/post_detail.html', {'post': post, 'user': request.user})

def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'blog_app/create_user.html', {'form': form})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'blog_app/create_category.html', {'form': form})

@login_required
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

def user_list(request):
    users = User.objects.annotate(post_count=Count('posts'))
    return render(request, 'blog_app/user_list.html', {'users': users})

def about(request):
    return render(request, 'blog_app/about.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'blog_app/login.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('home')
    post.delete()
    return redirect('home')

@login_required
def confirm_delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('home')
    return render(request, 'blog_app/confirm_delete_post.html', {'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        post.delete()  
        return redirect('home') 
    return redirect('home') 

def logout_view(request):
    logout(request)
    return redirect('home')


