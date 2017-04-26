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

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
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
                'message':'pikachu pika pika',
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
