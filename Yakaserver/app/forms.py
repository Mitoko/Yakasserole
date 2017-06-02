"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import *

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))



class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recette
        exclude = ('user',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('user', 'recipe',)

class AtelierCommentForm(forms.ModelForm):
    class Meta:
        model = AtelierComment
        exclude = ('user', 'atelier',)

#     nom = forms.CharField(max_length=100)
#     preparation = forms.DurationField()
#     cuisson = forms.DurationField()
#     ingredients =forms.CharField(widget=forms.Textarea)
#     recette = forms.CharField(widget=forms.Textarea)
