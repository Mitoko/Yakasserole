# -*- coding: utf-8 -*-
"""
Definition of models.
"""
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

import hashlib

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User)
    # recipe = models.ForeignKey(Recette)
    creation_date = models.DateTimeField(auto_now=True, blank=True)


class AtelierComment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now=True, blank=True)


class Atelier(models.Model):
    nom = models.CharField(max_length=100)
    chef = models.ForeignKey(User)
    date = models.DateTimeField(default=datetime.now()) #FIXME
    duration = models.DurationField()
    place = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    lieu = models.CharField(max_length=100) #FIXME list de lieu ?
    description = models.TextField()
    comments = models.ManyToManyField(AtelierComment)
    picture = models.CharField(max_length=300, blank=True)
    def get_absolute_url(self):
        return reverse('atelier', kwargs={'pk': self.pk})

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
    ingredients = models.TextField()
    recetteDetail = models.TextField()
    creation_date = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey(User)
    picture = models.CharField(max_length=300, blank=True)
    comments = models.ManyToManyField(Comment)
    def get_absolute_url(self):
        return reverse('recipe', kwargs={'pk': self.pk})



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    connections = models.DecimalField(max_digits=15, decimal_places=0, default=0)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

# Create your models here.
