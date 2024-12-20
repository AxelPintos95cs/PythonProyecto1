from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm, PostForm, Profile, ProfileForm, CustomPasswordChangeForm, CommentForm
from .models import Post, Like, Comment
from blog_app.models import Post, Category, Author
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import update_session_auth_hash

def home(request):
    posts = Post.objects.all().order_by('-created_at')[:5]  
    return render(request, 'blog_app/home.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_count = Like.objects.filter(post=post).count()
    comments = post.comments.all()  # Aseguramos que estamos obteniendo todos los comentarios asociados al post
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user  # Aseguramos que el comentario tiene al autor correcto
            new_comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'blog_app/post_detail.html', {
        'post': post,
        'like_count': like_count,
        'comments': comments,  # Pasamos los comentarios para el template
        'new_comment': new_comment,
        'comment_form': comment_form,
    })




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
    author_id = request.GET.get('author', '')  # Cambié 'author' por 'author_id'

    posts = Post.objects.all()  # Comienza con todos los posts

    # Filtra por título si hay una consulta de búsqueda
    if query:
        posts = posts.filter(title__icontains=query)
    
    # Filtra por categoría si hay una categoría seleccionada
    if category:
        posts = posts.filter(category__name__icontains=category)

    # Filtra por autor si hay un autor seleccionado
    if author_id:
        posts = posts.filter(author__id=author_id)

    # Obtiene los autores registrados que tienen al menos un post
    authors = User.objects.filter(posts__isnull=False).distinct()

    # Si se selecciona un autor, se comprueba si tiene posts
    selected_author = None
    if author_id:
        selected_author = User.objects.get(id=author_id)
        if not selected_author.posts.exists():
            posts = []  # Si no tiene posts, dejamos la lista de posts vacía

    # Si no hay posts después de la búsqueda, muestra el mensaje correspondiente
    no_posts_message = None
    if author_id and not posts:
        no_posts_message = "Este usuario aún no ha realizado ningún post."

    # Obtener todas las categorías para el filtro
    categories = Category.objects.all()

    return render(request, 'blog_app/search_results.html', {
        'posts': posts,
        'authors': authors,
        'categories': categories,
        'query': query,
        'category': category,
        'author_id': author_id,
        'selected_author': selected_author,
        'no_posts_message': no_posts_message,  # Pasamos el mensaje
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

@login_required

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    

    if not Like.objects.filter(user=request.user, post=post).exists():
        # Si no, crea un nuevo like
        Like.objects.create(user=request.user, post=post)

    # Después de crear el "like", redirige al detalle del post
    return redirect('post_detail', post_id=post.id)

@login_required
def my_account(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('my_account')

        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user) 
            return redirect('my_account')

    else:
        profile_form = ProfileForm(instance=profile)
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'blog_app/my_account.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })
