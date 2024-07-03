from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from posts.forms import PostForm
from posts.models import Post


def home_view(request):
    users = User.objects.all()
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')

    return render(request, 'posts/home.html', {'posts': posts, 'form': form,'users': users})


def post_view(request):
    return render(request,  "posts/post.html")