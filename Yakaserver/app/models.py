"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
import hashlib

class Recette(models.Model):
    nom = models.CharField(max_length=100)
    preparation = models.DurationField()
    cuisson = models.DurationField()
    ingredients = models.CharField(max_length=300)
    recette = models.CharField(max_length=800)
    creation_date = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey(User)

 
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

# Create your models here.
