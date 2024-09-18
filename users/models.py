
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=24)
