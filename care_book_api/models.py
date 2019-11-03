from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save

from django.db import models

class Allergy(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name_plural = 'allergies'

    def __str__(self):
        return self.name


class Home(models.Model):
    parents = models.ManyToManyField(User, related_name = 'parent')
    caretakers = models.ManyToManyField(User, related_name = 'caretaker')
    name = models.CharField(max_length = 150, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Child(models.Model):
    name = models.CharField(max_length = 150)
    image = models.ImageField(null=True, blank=True)
    dob = models.DateField()
    medical_history = models.TextField()
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='children')
    allergies = models.ManyToManyField(Allergy, related_name='children')

    class Meta:
        verbose_name_plural = 'children'

    def __str__(self):
        return self.name


class Post(models.Model):
    children = models.ManyToManyField(Child, related_name='post')
    image = models.ImageField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

