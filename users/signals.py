import os
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver

def create_user_if_not_exists(username, password_env_var):
    password = os.environ.get(password_env_var)
    if not password:
        raise ValueError(f"Environment variable '{password_env_var}' is not set.")
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.save()
        print(f"User '{username}' created.")
    else:
        print(f"User '{username}' already exists.")

@receiver(post_migrate)
def create_default_users(sender, **kwargs):
    create_user_if_not_exists('machinegod', 'password_user')
    create_user_if_not_exists('guest', 'password_user')
