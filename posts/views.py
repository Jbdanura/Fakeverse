from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from generateAI import generate
from posts.forms import PostForm, CommentForm
from posts.models import Post, Comment
from django.db.models import Count
from users.models import Profile
import random
from django.core.paginator import Paginator
import cloudinary.uploader
import requests

def home_view(request):

    if request.GET.get('view') == 'following':
        following_users = request.user.profile.following.all()
        posts_list = Post.objects.filter(author__profile__in=following_users).order_by('-created_at')
    else:
        posts_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    comment_form = CommentForm()
    new_users = User.objects.order_by('-date_joined')[:5]
    top_users = Profile.objects.annotate(num_followers=Count('followers')).order_by('-num_followers')[:5]

    return render(request, 'posts/home.html',
                  {'posts': posts,
                   'comment_form':comment_form,
                   'new_users':new_users,
                   'top_users':top_users
                   })

@login_required
def create_post(request):
    generatedPost = generate()
    if generatedPost:
        AI_user = get_object_or_404(User,username="machinegod")
        AI_post = Post(author=AI_user, content=generatedPost)
        AI_post.save()
    if request.method == 'POST':
        form = PostForm(request.POST)
        print(request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            if request.FILES.get('image'):
                file = request.FILES['image']
                upload_result = cloudinary.uploader.upload(file, public_id=f'post_{post.id}',folder='fakeverse')
                print(upload_result)
                post.image = upload_result['url']
                post.save(update_fields=['image'])

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
        else:
            messages.error(request,"Invalid post")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')
    return redirect('home')

@login_required
def add_comment(request,post_id):
    generatedPost = generate()
    if generatedPost:
        AI_user = get_object_or_404(User,username="machinegod")
        AI_post = Post(author=AI_user, content=generatedPost)
        AI_post.save()
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
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
    return redirect("home")

@login_required
def like_post(request,post_id):
    generatedPost = generate()
    if generatedPost:
        AI_user = get_object_or_404(User,username="machinegod")
        AI_post = Post(author=AI_user, content=generatedPost)
        AI_post.save()
    post = get_object_or_404(Post,id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        messages.success(request, "Post disliked")
    else:
        post.likes.add(request.user)
        messages.success(request, "Post liked")
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)

@login_required
def edit_post(request, post_id):
    generatedPost = generate()
    if generatedPost:
        AI_user = get_object_or_404(User,username="machinegod")
        AI_post = Post(author=AI_user, content=generatedPost)
        AI_post.save()
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        if post.author != request.user:
            messages.error(request, "You are not authorized to edit this post.")
            return redirect('home')
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
    else:
        return redirect("home")
    return redirect("home")

@login_required
def delete_post(request, post_id):
    generatedPost = generate()
    if generatedPost:
        AI_user = get_object_or_404(User,username="machinegod")
        AI_post = Post(author=AI_user, content=generatedPost)
        AI_post.save()
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('home')
    post.delete()
    messages.success(request, "Post deleted successfully.")
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    else:
        return redirect('home')




@login_required
def delete_comment(request, comment_id):
    generatedPost = generate()
    if generatedPost:
        AI_user = get_object_or_404(User,username="machinegod")
        AI_post = Post(author=AI_user, content=generatedPost)
        AI_post.save()
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        messages.error(request, "You are not authorized to delete this comment.")
        return redirect('home')
    comment.delete()
    messages.success(request, "Comment deleted successfully")
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    else:
        return redirect('home')

def load_more_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    context = {'comments': comments, 'user': request.user}
    comments_html = render_to_string('posts/comments_list.html', context)
    return JsonResponse({'comments_html': comments_html})





