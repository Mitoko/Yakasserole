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
    recetteDetail = models.CharField(max_length=800)
    creation_date = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey(User)
    picture = models.ImageField(verbose_name='Image', upload_to='images', null=True, blank=True)
 
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

# Create your models here.
