from django.db import models
from django.contrib.auth.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage  # Cloudinary storage

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Use Cloudinary storage for profile pictures
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True,
        storage=MediaCloudinaryStorage()
    )
    full_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
