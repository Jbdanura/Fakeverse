from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from posts.models import Post
from django.contrib import messages
from django.db import transaction

def allusers_view(request):
    users = User.objects.all()
    return render(request, "users/allusers.html",{"users":users})



@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    posts = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, 'users/profile.html', {'profile': profile, 'posts': posts})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', {'form': form})


def search_user(request):
    query = request.GET.get('query')
    if query:
        user = User.objects.filter(username__iexact=query).first()
        if user:
            return redirect('view_profile', user.username)
        else:
            return render(request, 'user_not_found.html')
    return redirect('home')

@login_required
@transaction.atomic
def follow_unfollow(request, username):
    if request.user.username == username:
        messages.error(request, "You can't follow yourself.")
        return redirect('view_profile', username=username)

    target_user = get_object_or_404(User, username=username)
    user_profile = request.user.profile
    target_profile = target_user.profile  # Get the Profile instance instead of User

    if target_profile in user_profile.following.all():
        user_profile.following.remove(target_profile)
        messages.success(request, f"You have unfollowed {username}.")
    else:
        user_profile.following.add(target_profile)
        messages.success(request, f"You are now following {username}.")

    next_url = request.GET.get('next')
    return redirect(next_url or 'view_profile', username=username)