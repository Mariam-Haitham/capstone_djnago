from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save

from django.db import models

class Allergy(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = 'allergies'

    def __str__(self):
        return self.name


class Home(models.Model):
    parents = models.ManyToManyField(User, related_name = 'parent')
    caretakers = models.ManyToManyField(User, related_name = 'caretaker')


class Child(models.Model):
    name = models.CharField(max_length = 150)
    image = models.ImageField(null=True, blank=True)
    dob = models.DateField()
    medical_history = models.TextField()
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    allergies = models.ManyToManyField(Allergy, related_name='children')

    class Meta:
        verbose_name_plural = 'children'

    def __str__(self):
        return self.name


class Post(models.Model):
    image = models.ImageField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
