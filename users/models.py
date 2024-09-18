from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageOps
import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        profile_img = Image.open(self.profile_pic.path)
        if profile_img.height > 300 or profile_img.width > 300:
            output_size = (300, 300)
            # profile_img.thumbnail(output_size)  # resized to 300x300 but skews not square images
            resized_image = ImageOps.fit(profile_img, output_size)
            resized_image.save(self.profile_pic.path)
