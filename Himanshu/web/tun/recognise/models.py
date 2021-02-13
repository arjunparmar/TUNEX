from django.db import models

# Create your models here.
import os

class Image(models.Model):
    image=models.ImageField(upload_to="up_img/")
    caption = models.CharField(max_length=100)
    def __str__(self):
        return self.caption 