from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username}'s profile."

    def save(self, *args, **kwargs):  # overriding method inherited from models.Model
        super().save(*args, **kwargs)  # calls the save() from Model - saves the pic stored in image var
        img = Image.open(self.image.path)  # uses the imported Image from PILlow to open the image by its path (.path is inherited from Model)
        if img.height > 300 or img.width > 300:  # if any of the dimensions is bigger than 300 px
            output_size = (300, 300)  # save a tuple with the desired dimensions
            img.thumbnail(output_size)
            img.save(self.image.path)  # save the image with new dimensions and replace the old img with smaller in filesystem