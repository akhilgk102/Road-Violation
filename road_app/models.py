from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    phone=models.CharField(max_length=12)


class RoadViolation(models.Model):

    description=models.TextField(max_length=500)    

    image=models.ImageField(upload_to="violation_images")

    created_at=models.DateTimeField(auto_now_add=True)

    owner=models.ForeignKey(User,on_delete=models.CASCADE)