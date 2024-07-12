from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from posts.forms import PostForm, CommentForm
from posts.models import Post, Comment


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

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        if post.author != request.user:
            messages.error(request, "You are not authorized to edit this post.")
            return redirect('home')
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('home')
    else:
        return redirect("home")

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('home')
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('home')




@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        messages.error(request, "You are not authorized to delete this comment.")
        return redirect('home')
    comment.delete()
    messages.success(request, "Comment deleted successfully")
    return redirect('home')
