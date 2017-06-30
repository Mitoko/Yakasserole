# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import *
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.extras.widgets import *


class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

    # nom = models.CharField(max_length=100)
    # difficulte = models.CharField(
    #     max_length=1,
    #     choices=DIFFICULTY_CHOICES,
    #     default='F',
    # )
    # type = models.CharField(
    #     max_length=1,
    #     choices=TYPE_CHOICES,
    #     default='E',

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

class RecipeForm(forms.ModelForm):
    nom = forms.CharField(label='Nom de la recette')
    # difficulte = forms.ChoiceField(label='Difficulté: ')
    # type = forms.ChoiceField(label='Type: ', choices:)
    cuisson = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Temps de cuisson')
    preparation = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Temps de préparation')
    ingredients = forms.CharField(label='Liste des ingrédients', widget=forms.Textarea)
    recetteDetail = forms.CharField(label='Détail de la recette', widget=forms.Textarea)
    class Meta:
        model = Recette
        exclude = ('user', 'comments', 'creation_date', 'picture')
        help_texts = {
            'cuisson': 'Format: HH:MM',
            'preparation': 'Format: HH:MM',
        }


class AtelierForm(forms.ModelForm):
    nom = forms.CharField(label='Nom de l\'atelier')
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Heure')
    # chef = models.ForeignKey(User)
    duration = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Durée de l\'atelier')
    prix = forms.DecimalField( min_value=0, max_digits=2, label='Prix (en €)')
    place = forms.IntegerField(min_value=0, label='Nombre de place')
    # lieu = models.CharField(max_length=100) #FIXME list de lieu ?

    class Meta:
        model = Atelier
        exclude = ('restant', 'comments', 'picture')
        help_texts = {
            'duration': 'Format: HH:MM',
        }
    def __init__(self, *args, **kwargs):
        super(AtelierForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['chef'].queryset = User.objects.filter(groups__name='Chef Cuisinier')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)
        # '__all__'

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'groups')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('user', 'recipe',)


class NoteForm(forms.ModelForm):
    class Meta:
        model = Notation
        exclude = ('user', 'recette',)

class AtelierCommentForm(forms.ModelForm):
    class Meta:
        model = AtelierComment
        exclude = ('user', 'atelier',)
