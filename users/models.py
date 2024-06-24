from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    directory_path = models.CharField(max_length=255, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.directory_path:
            self.directory_path = f'user_{self.user.id}'
        super().save(*args, **kwargs)

    def create_user_directory(self):
        user_folder = os.path.join(settings.MEDIA_ROOT, self.directory_path)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

    def __str__(self):
        return self.user.username
