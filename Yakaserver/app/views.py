# -*- coding: utf-8 -*-
"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponse
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from allauth.socialaccount.models import SocialAccount
from .forms import RecipeForm
from .models import Recette

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def recettes(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/recettes.html',
        {
            'title':'Recettes',
            'message':'Les recettes',
            'year':datetime.now().year,
        }
    )

def ateliers(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/ateliers.html',
        {
            'title':'Ateliers',
            'message':'Les ateliers',
            'year':datetime.now().year,
        }
    )

def apropos(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/apropos.html',
        {
            'title':'A propos',
            'message':'A propos de nous',
            'year':datetime.now().year,
        }
    )



def user(request):
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated():
        return render(
            request,
            'app/user.html',
            {
                'firstname': request.user.first_name,
                'lastname': request.user.last_name,
                'email': request.user.email,
                'message':'Utilisateur',
                'lastlogin': request.user.last_login,
                'datejoined': request.user.date_joined,
                'year':datetime.now().year,
            }
        )
    else:
        return render(
            request,
            'app/login.html'
        )
    # return HttpResponse(username)




def recipeform(request):
    form = RecipeForm(request.POST or None)
    if form.is_valid():
        nom = form.cleaned_data.get('Nom de la recette')
        preparation = form.cleaned_data.get('Temps de préparation')
        cuisson = form.cleaned_data.get('Temps de cuisson')
        ingredients = form.cleaned_data.get('Ingrédients')
        recette = form.cleaned_data.get('Détails de la recette')
        form.save()
    return render(request, 'app/newrecipe.html', locals())
