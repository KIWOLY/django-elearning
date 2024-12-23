from django.contrib.auth.models import User
from django.db import models
import uuid

# Models
class Student(models.Model):
    DEFAULT_FIRSTNAME = "John"
    DEFAULT_LASTNAME = "Doe"

    firstname = models.CharField(max_length=50, default=DEFAULT_FIRSTNAME)
    lastname = models.CharField(max_length=50, default=DEFAULT_LASTNAME)
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)

    def __str__(self):
        return self.firstname

class Number(models.Model):
    number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.number

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    registration_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        reg_number = self.registration_number if self.registration_number else 'No Reg Number'
        phone = self.phone if self.phone else 'No Phone'
        category = self.category if self.category else 'No Category'
        return f"{self.user.username} - Reg: {reg_number}, Phone: {phone}, Category: {category}"


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Note(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notes', default=1)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='notes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
    def __str__(self):
        return self.title

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"

