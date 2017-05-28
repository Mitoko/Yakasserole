# -*- coding: utf-8 -*-
"""
Definition of models.
"""
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
import hashlib

class Recette(models.Model):
    nom = models.CharField(max_length=100)
    FACILE = 'F'
    MOYEN = 'M'
    DIFFICILE = 'D'
    DIFFICULTY_CHOICES = (
        (FACILE, 'Facile'),
        (MOYEN, 'Moyen'),
        (DIFFICILE, 'Difficile'),
    )
    difficulte = models.CharField(
        max_length=1,
        choices=DIFFICULTY_CHOICES,
        default=FACILE,
    )

    ENTREE = 'E'
    PLAT = 'P'
    DESSERT = 'D'
    TYPE_CHOICES = (
        (ENTREE, 'Entrée'),
        (PLAT, 'Plat'),
        (DESSERT, 'Dessert'),
    )
    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default=ENTREE,
    )

    preparation = models.DurationField()
    cuisson = models.DurationField()
    ingredients = models.CharField(max_length=300)
    recetteDetail = models.CharField(max_length=800)
    creation_date = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey(User)
    picture = models.ImageField(verbose_name='Image', upload_to='images', null=True, blank=True)
    def get_absolute_url(self):
        return reverse('recipe', kwargs={'pk': self.pk})

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

# Create your models here.
