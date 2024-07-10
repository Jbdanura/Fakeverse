from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from posts.forms import PostForm, CommentForm
from posts.models import Post


def home_view(request):
    users = User.objects.all()
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()
    comment_form = CommentForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')

    return render(request, 'posts/home.html',
                  {'posts': posts,
                   'form': form,
                   'users': users,
                   'comment_form':comment_form
                   })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    return redirect('home')

@login_required
def add_comment(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    print(request.POST)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment added")
            return redirect("home")
    return redirect("home")

@login_required
def like_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        messages.success(request, "Post unliked")
    else:
        post.likes.add(request.user)
        messages.success(request, "Post liked")
    return redirect("home")


def get_more_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    offset = int(request.GET.get('offset', 0))
    limit = 5
    comments = post.comments.all()[offset:offset + limit]

    comments_data = [{
        'author': comment.author.username,
        'content': comment.content,
        'updated_at': comment.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    } for comment in comments]

    return JsonResponse({'comments': comments_data})