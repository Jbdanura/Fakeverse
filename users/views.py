from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import BioEditForm, AvatarEditForm
from posts.models import Post
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.safestring import mark_safe

def allusers_view(request):
    users = User.objects.all()
    return render(request, "users/allusers.html",{"users":users})



@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    posts_list = Post.objects.filter(author=user).order_by('-created_at')
    paginator = Paginator(posts_list, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'users/profile.html', {'profile': profile, 'posts': posts})


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

@login_required
def edit_profile(request):
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            form = BioEditForm(request.POST, instance=request.user.profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile has been updated!')
            else:
                error_messages = []
                for field, errors in form.errors.items():
                    error_messages.append(f"{field.capitalize()}: {', '.join(errors)}")
                messages.error(request, f"Error updating profile: {'; '.join(error_messages)}")
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
            else:
                messages.error(request, "Error changing password")
        return redirect('edit_profile')
    else:
        form = BioEditForm(instance=request.user.profile)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'users/edit_profile.html', {
        'form': form,
        'password_form': password_form
    })

@login_required
def edit_avatar(request):
    if request.method == "POST":
        if not request.FILES:
            messages.error(request,"No image submitted")
            return redirect('edit_profile')
        form = AvatarEditForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Your avatar was successfully updated!")
        else:
            messages.error(request,"Error changing avatar")
    return redirect('edit_profile')