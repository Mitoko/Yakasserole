# -*- coding: utf-8 -*-
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

import hashlib

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now=True, blank=True)


class AtelierComment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now=True, blank=True)


class Atelier(models.Model):
    nom = models.CharField(max_length=100)
    chef = models.ForeignKey(User) #Must be Chiefs only
    date = models.DateField() #FIXME
    time = models.TimeField()
    duration = models.TimeField()
    prix = models.DecimalField(max_digits=15, decimal_places=2)
    place = models.DecimalField(max_digits=15, decimal_places=0)
    restant = models.DecimalField(max_digits=15, decimal_places=0)
    lieu = models.CharField(max_length=100) #FIXME list de lieu ?
    description = models.TextField()
    comments = models.ManyToManyField(AtelierComment)
    picture = models.ImageField(upload_to = 'static/app/images/', default = 'static/app/images/default.png')
    def get_absolute_url(self):
        return reverse('atelier', kwargs={'pk': self.pk})


class AtelierInscription(models.Model):
    atelier = models.ForeignKey(Atelier)
    user = models.ForeignKey(User)
    nbplace = models.DecimalField(max_digits=15, decimal_places=0, default=1)
#prixtotal
#check user
#if pas inscrit, display bouton (html)
#bouton s'inscrire:
# si premium ? nb place
# paiement
# créer AtelierInscription
# attention: nb place restants

class Recette(models.Model):
    nom = models.CharField(max_length=100)
    DIFFICULTY_CHOICES = (
        ('F', 'Facile'),
        ('M', 'Moyen'),
        ('D', 'Difficile'),
    )
    difficulte = models.CharField(
        max_length=1,
        choices=DIFFICULTY_CHOICES,
        default='F',
    )
    TYPE_CHOICES = (
        ('E', 'Entrée'),
        ('P', 'Plat'),
        ('D', 'Dessert'),
    )
    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default='E',
    )

    preparation = models.TimeField()
    cuisson = models.TimeField()
    ingredients = models.TextField()
    recetteDetail = models.TextField()
    creation_date = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey(User)
    picture = models.ImageField(upload_to = 'static/app/images/', default = 'static/app/images/default.png')
    comments = models.ManyToManyField(Comment)
    def get_absolute_url(self):
        return reverse('recipe', kwargs={'pk': self.pk})


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    connections = models.DecimalField(max_digits=15, decimal_places=0, default=0)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
