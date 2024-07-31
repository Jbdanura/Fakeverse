import os
from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.db.models.signals import post_save
from django.dispatch import receiver

def user_avatar_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Create the new filename using the user's id
    filename = f'avatar_{instance.user.id}.{ext}'
    # Return the full path
    return os.path.join('avatars', filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_avatar_path, default='avatars/default.jpg')
    bio = models.TextField(blank=True,max_length=100)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()