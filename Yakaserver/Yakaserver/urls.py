"""
Definition of urls for Yakaserver.
"""

from datetime import datetime
from django.conf.urls import include, url
from django.contrib import admin
import django.contrib.auth.views
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    # url(r'^recettes/new/$', app.views.recipeform, name='recipeform'),
    url(r'^recettes/new/$', app.views.RecipeCreate.as_view(), name='recipeform'),


    url(r'^recettes/search/entree$', app.views.recipeEntree, name='recipe-entree'),
    url(r'^recettes/search/plat$', app.views.recipePlat, name='recipe-plat'),
    url(r'^recettes/search/dessert$', app.views.recipeDessert, name='recipe-dessert'),
    url(r'^recettes/search/nouveaute$', app.views.recipeNew, name='recipe-new'),
    url(r'^recettes/search/populaires$', app.views.recipeNew, name='recipe-pop'),
#    url(r'^recettes/search/$', app.views.recipeEntree, name='recipe-entree'),
    url(r'^recettes/(?P<pk>\d+)/edit/$', app.views.RecipeUpdate.as_view(), name='recipe-update'),
    url(r'^recettes/(?P<pk>\d+)/delete/$', app.views.RecipeDelete.as_view(), name='recipe-delete'),
    url(r'^recettes/(?P<pk>\d+)/comment/(?P<pkcomment>\d+)/$', app.views.commentDelete, name='comment-delete'),
    url(r'^recettes/(?P<pk>\d+)/$', app.views.recipe, name='recipe'),
    url(r'^recettes/$', app.views.recettes, name='recettes'),

    url(r'^ateliers/new/$', app.views.AtelierCreate.as_view(), name='atelierform'),
    url(r'^ateliers/(?P<pk>\d+)/inscription/(?P<nb>[1-4])/$', app.views.atelierPaiement, name='atelier-paiement'),
    url(r'^ateliers/(?P<pk>\d+)/inscription/$', app.views.atelierInscription, name='atelier-inscription'),
    url(r'^ateliers/(?P<pk>\d+)/edit/$', app.views.AtelierUpdate.as_view(), name='atelier-update'),
    url(r'^ateliers/(?P<pk>\d+)/delete/$', app.views.AtelierDelete.as_view(), name='atelier-delete'),
    url(r'^ateliers/(?P<pk>\d+)/comment/(?P<pkcomment>\d+)/$', app.views.ateliercommentDelete, name='ateliercomment-delete'),
    url(r'^ateliers/(?P<pk>\d+)/$', app.views.atelier, name='atelier'),
    url(r'^ateliers/$', app.views.ateliers, name='ateliers'),
    url(r'^apropos', app.views.apropos, name='apropos'),
    url(r'^login/$',
         django.contrib.auth.views.login,
         {
             'template_name': 'app/login.html',
             'authentication_form': app.forms.BootstrapAuthenticationForm,
             'extra_context':
             {
                 'title': 'Log in',
                 'year': datetime.now().year,
             }
         },
         name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {

            'next_page': '/',
        },
        name='logout'),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', RedirectView.as_view(pattern_name='home', permanent=False)),
    # url(r'^user/(?P<user.username>w+)/', app.views.user, name='user'),
    url(r'^user/profile/', app.views.user, name='user'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
     url(r'^admin/', admin.site.urls),
]
