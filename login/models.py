from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


# Create your models here.
class Student(models.Model):
    DEFAULT_FIRSTNAME = "John"
    DEFAULT_LASTNAME = "Doe"

    firstname=models.CharField(max_length=50, default=DEFAULT_FIRSTNAME )
    lastname=models.CharField(max_length=50 , default=DEFAULT_LASTNAME )
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)

    def __str__(self):
        return self.firstname


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Note(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='notes/')
    uploaded_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title



class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name