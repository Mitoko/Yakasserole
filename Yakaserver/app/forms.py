"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

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



class RecipeForm(forms.Form):
    nom = forms.CharField(max_length=100)
    preparation = forms.DurationField()
    cuisson = forms.DurationField()
    ingredients =forms.CharField(widget=forms.Textarea)
    recette = forms.CharField(widget=forms.Textarea)

    #auteur

#
# class ContactForm(forms.Form):
#     sujet = forms.CharField(max_length=100)
#     message = forms.CharField(widget=forms.Textarea)
#     envoyeur = forms.EmailField(label="Votre adresse mail")
#     renvoi = forms.BooleanField(help_text="Cochez si vous souhaitez obtenir une copie du mail envoye.", required=False)
