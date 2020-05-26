from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # username is national-id
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)