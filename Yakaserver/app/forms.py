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
    # )
    #
    # preparation = models.DurationField()
    # cuisson = models.DurationField()
    # ingredients = models.TextField()
    # recetteDetail = models.TextField()
    # picture = models.CharField(max_length=300, blank=True)

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recette
        exclude = ('user', 'comments', 'creation_date', 'picture')
    # def __init__(self, *args, **kwargs):
    #     super(RecipeForm, self).__init__(*args, **kwargs)
    #     self.fields['da'].widget = widgets.AdminDateWidget()

class AtelierForm(forms.ModelForm):
    # date = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker', format="%Y-%m-%d"}))

    class Meta:
        model = Atelier
        exclude = ('restant', 'comments', 'picture')
    def __init__(self, *args, **kwargs):
        super(AtelierForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['chef'].queryset = User.objects.filter(groups__name='Chef cuisinier')

    # # date_field = forms.DateField(widget=AdminDateWidget)
    # widgets = {
    #     # 'date': forms.DateInput(attrs={'class': 'datepicker'})
    #     'date': forms.DateInput(attrs={'class': 'datepicker', 'id': 'date',})
    # }
    # def __init__(self, *args, **kwargs):
    #     super(AtelierForm, self).__init__(*args, **kwargs)
    #     self.fields['date'].widget = widgets.AdminDateWidget()

    # nom = models.CharField(max_length=100)
    # chef = models.ForeignKey(User)
    # date = models.DateTimeField(default=datetime.now()) #FIXME
    # duration = models.DurationField()
    # prix = models.DecimalField(max_digits=15, decimal_places=2)
    # place = models.DecimalField(max_digits=15, decimal_places=0)
    # lieu = models.CharField(max_length=100) #FIXME list de lieu ?
    # description = models.TextField()
    # picture = models.CharField(max_length=300, blank=True)

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
