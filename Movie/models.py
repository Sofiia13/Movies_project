from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class TodoItem(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class Movie(models.Model):
    title = models.CharField(max_length=100)