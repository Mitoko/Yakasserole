# -*- coding: utf-8 -*-
from django.db.models.signals import pre_delete
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponse
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from allauth.socialaccount.models import SocialAccount
from .forms import *
from .models import Recette, Comment
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.dispatch.dispatcher import receiver
from allauth.account.signals import user_logged_in
from django.shortcuts import redirect


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
            'recipenb': Recette.objects.filter().count(),
            'commentnb': Comment.objects.filter().count()
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
                'connections': request.user.profile.connections,
                'recipenb': Recette.objects.filter(user=request.user).count(),
                'commentnb': Comment.objects.filter(user=request.user).count()
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
    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.user = self.request.user
        if not recipe.picture:
            recipe.picture = "/static/app/images/default.png"
        recipe.save()
        return super(RecipeCreate, self).form_valid(form)

class RecipeUpdate(UpdateView):
    model = Recette
    fields = ['nom', 'difficulte', 'type', 'preparation', 'cuisson', 'ingredients', 'recetteDetail', 'picture']
    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.user = self.request.user
        if recipe.picture:
            recipe.picture = "/static/app/images/default.png"
        recipe.save()
        return super(RecipeUpdate, self).form_valid(form)


class RecipeDelete(DeleteView):
    model = Recette
    success_url = reverse_lazy('recettes')

@login_required(login_url='/')
def recipe(request, pk):
    recipe = Recette.objects.get(pk=pk)
    comments = recipe.comments.all()
    #content = request.POST.get('text_box')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.data['content']
            # recette = Recette.objects.get(pk=pk)
            post = Comment.objects.create(content=content, user=request.user)
            recipe.comments.add(post)
            return render(request, 'app/recipe.html', {'recipe':recipe, 'comments':comments, 'form':CommentForm()})
    else:
        form = CommentForm()
    return render(request, 'app/recipe.html', {'recipe':recipe, 'comments':comments, 'form':form})

@login_required(login_url='/')
def commentDelete(request, pk, pkcomment):
    Comment.objects.get(id=pkcomment).delete()
    return redirect('recipe', pk)

@login_required(login_url='/')
def recipeEntree(request):
    recipes = Recette.objects.filter(type='E')
    return render(request, 'app/listrecettes.html', {'recettes':recipes, 'message':'Les entrées'})

@login_required(login_url='/')
def recipePlat(request):
    recipes = Recette.objects.filter(type='P')
    return render(request, 'app/listrecettes.html', {'recettes':recipes, 'message':'Les plats'})

@login_required(login_url='/')
def recipeDessert(request):
    recipes = Recette.objects.filter(type='D')
    return render(request, 'app/listRecettes.html', {'recettes':recipes, 'message':'Les desserts'})

@login_required(login_url='/')
def recipeNew(request):
    recipes = Recette.objects.order_by('creation_date')
    return render(request, 'app/listRecettes.html', {'recettes':recipes, 'message':'Nouveautés'})

@login_required(login_url='/')
def recipePop(request):
    recipes = Recette.objects.annotate(commentnb=Count('comments')).order_by('-commentnb')
    return render(request, 'app/listRecettes.html', {'recettes':recipes, 'message':'Populaires'})

@receiver(user_logged_in, dispatch_uid="unique")
def user_logged_in_(request, user, **kwargs):
    mymodel = request.user.profile
    mymodel.connections = F('connections') + 1
    mymodel.save()


@receiver(pre_delete, sender=Recette)
def cascade_delete_branch(sender, instance, **kwargs):
    for t in instance.comments.all():
        t.delete()
