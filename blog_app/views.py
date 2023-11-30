from django.http import HttpResponseRedirect
from django.shortcuts import render
from blog_app.models import Post, Comment
from blog_app.forms import CommentForm, PostForm

def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post(
                title=form.cleaned_data['title'],
                body=form.cleaned_data['body'],
            )
            post.save()
            return HttpResponseRedirect(request.path_info)

    context = {
        'posts': posts,
        'form': PostForm(),
    }
    return render(request, 'blog/index.html', context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by('-created_on')
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category.html', context)

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data['author'],
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