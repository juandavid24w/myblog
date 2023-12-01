from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from blog_app.models import Post, Comment
from blog_app.forms import CommentForm, PostForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    
    form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = {
        'posts': posts,
    }
    return render(request, 'blog/index.html', context)

@login_required
def get_user_blogs(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_on')

    context = {
        'posts': posts,
    }
    return render(request, 'blog/my-blogs.html', context)

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Create a new post with the form data
            post = Post(
                title=form.cleaned_data['title'],
                body=form.cleaned_data['body'],
                author=request.user
            )
            post.save()

            return HttpResponseRedirect(reverse('blog_detail', args=[post.pk]))
    else:
        # Render an empty form for creating a new post
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'blog/create.html', context)

@login_required
def update_blog(request, id):
    post = Post.objects.get(id=id)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Update the existing post with the form data
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            post.save()

            return HttpResponseRedirect(reverse('blog_detail', args=[post.pk]))
    else:
        # Populate the form with the existing post data
        form = PostForm(initial={'title': post.title, 'body': post.body})

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/update.html', context)

@login_required
def delete_blog(request, id):
    Post.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('blog_index'))

@login_required
def blog_detail(request, id):
    post = Post.objects.get(id=id)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=request.user,
                body=form.cleaned_data['body'],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'comments': comments,
        'form': CommentForm(),
    }

    return render(request, 'blog/detail.html', context)