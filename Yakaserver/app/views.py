# -*- coding: utf-8 -*-


"""
Definition of views.
"""
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponse
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from allauth.socialaccount.models import SocialAccount
from .forms import RecipeForm
from .models import Recette
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='/')
def recettes(request, recipe_form=None):
    recipe_form = recipe_form or RecipeForm()
    recettes = Recette.objects.reverse()[:6]
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/recettes.html',
        {
            'recipe_form': recipe_form,
            'next_url': '/recettes',
            'recettes': recettes,
            'username': request.user.username
        }
    )

@login_required(login_url='/')
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

@login_required(login_url='/')
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


@login_required(login_url='/')
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


class RecipeCreate(CreateView):
    model = Recette
    fields = ['nom', 'difficulte', 'type', 'preparation', 'cuisson', 'ingredients', 'recetteDetail', 'picture']
    #if form.is_valid():
    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.user = self.request.user
        return super(RecipeCreate, self).form_valid(form)


class RecipeUpdate(UpdateView):
    model = Recette
    fields = ['nom', 'difficulte', 'type', 'preparation', 'cuisson', 'ingredients', 'recetteDetail', 'picture']
    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.user = self.request.user
        return super(RecipeUpdate, self).form_valid(form)


class RecipeDelete(DeleteView):
    model = Recette
    success_url = reverse_lazy('recettess')

@login_required(login_url='/')
def recipe(request, pk):
    recipes = Recette.objects.filter(pk=pk)
    return render(request, 'app/recipe.html', {'recipes':recipes})


@login_required(login_url='/')
def recipeEntree(request):
    recipes = Recette.objects.filter(type='E')
    return render(request, 'app/listrecettes.html', {'recettes':recipes})

@login_required(login_url='/')
def recipePlat(request):
    recipes = Recette.objects.filter(type='P')
    return render(request, 'app/listrecettes.html', {'recettes':recipes})

@login_required(login_url='/')
def recipeDessert(request):
    recipes = Recette.objects.filter(type='D')
    return render(request, 'app/listRecettes.html', {'recettes':recipes})

@login_required(login_url='/')
def recipeNew(request):
    recipes = Recette.objects.order_by('creation_date')
    return render(request, 'app/listRecettes.html', {'recettes':recipes})
