# -*- coding: utf-8 -*-
import xlwt
from django.http import HttpResponse
from django.contrib.auth.models import User
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
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import F
from django.db.models import Q
from django.db.models import Count
from django.dispatch.dispatcher import receiver
from allauth.account.signals import user_logged_in
from django.shortcuts import redirect
import operator
from django.core.mail import send_mail
from django.db.models import Sum
from itertools import chain
from django.core.exceptions import ObjectDoesNotExist
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    ateliers = Atelier.objects.order_by('date')[0:3]
    recettespop = Recette.objects.annotate(commentnb=Count('comments')).order_by('-commentnb')[:3]
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'recipenb': Recette.objects.filter().count(),
            'acommentnb': AtelierComment.objects.filter().count(),
            'rcommentnb': Comment.objects.filter().count(),
            'ateliernb': Atelier.objects.filter().count(),
            'clientnb': User.objects.filter(groups__name=None).count(),
            'prnb': User.objects.filter(groups__name='Client Premium').count(),
            'usernb': User.objects.filter().count(),
            'inscrnb': AtelierInscription.objects.filter().count(),
            'ateliers' : ateliers,
            'recettespop': recettespop
        }
    )

@login_required(login_url='/')
def recettes(request, recipe_form=None):
    recipe_form = recipe_form or RecipeForm()
    recettes = Recette.objects.reverse()[:6]
    recettespop = Recette.objects.annotate(commentnb=Count('comments')).order_by('-commentnb')[:3]
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/recettes.html',
        {
            'recipe_form': recipe_form,
            'next_url': '/recettes',
            'recettes': recettes,
            'recettespop': recettespop,
            'username': request.user.username
        }
    )

@login_required(login_url='/')
def ateliers(request):
    """Renders the about page."""
    ateliers = Atelier.objects.reverse()[:18]
    atelierspop = (Atelier.objects.annotate(commentnb=Count('comments'))).order_by('-commentnb')[:3]
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/ateliers.html',
        {
            'title':'Ateliers',
            'message':'Les ateliers',
            'ateliers':ateliers,
            'atelierspop':atelierspop
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
        inscrs = AtelierInscription.objects.filter(user=request.user)
        myAt = Atelier.objects.filter(chef=request.user)
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
                'commentnb': Comment.objects.filter(user=request.user).count(),
                'inscriptionsnb': AtelierInscription.objects.filter(user=request.user).count(),
                'inscrs': inscrs,
                'myAt': myAt
            }
        )
    else:
        return render(
            request,
            'app/login.html'
        )

@login_required(login_url='/')
def userprofile(request, pk):
    userid = User.objects.get(pk=pk)
    myAt = Atelier.objects.filter(chef=userid).order_by('date')
    inscrs = AtelierInscription.objects.filter(user=userid)
    return render(
            request,
            'app/userprofile.html',
            {
                'userid': userid,
                'firstname': userid.first_name,
                'lastname': userid.last_name,
                'email': userid.email,
                'message':'Utilisateur',
                'lastlogin': userid.last_login,
                'datejoined': userid.date_joined,
                'year':datetime.now().year,
                'connections': userid.profile.connections,
                'recipenb': Recette.objects.filter(user=userid).count(),
                'commentnb': Comment.objects.filter(user=userid).count(),
                'inscriptionsnb': AtelierInscription.objects.filter(user=userid).count(),
                'myAt' : myAt,
                'inscrs': inscrs
            }
        )


class RecipeCreate(CreateView):
    model = Recette
    form_class = RecipeForm
    # fields = ['nom', 'difficulte', 'type', 'preparation', 'cuisson', 'ingredients', 'recetteDetail', 'picture']
    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.user = self.request.user
        if not recipe.picture:
            recipe.picture = "/static/app/images/default.png"
        recipe.save()
        return super(RecipeCreate, self).form_valid(form)

class RecipeUpdate(UpdateView):
    model = Recette
    form_class = RecipeForm
    # fields = ['nom', 'difficulte', 'type', 'preparation', 'cuisson', 'ingredients', 'recetteDetail', 'picture']
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

def upload_pic(request, pk):
    if request.method == 'POST':
        form2 = ImageUploadForm(request.POST, request.FILES)
        if form2.is_valid():
            m = Recette.objects.get(pk=pk)
            m.picture = form2.cleaned_data['image']
            m.save()
        recipe = Recette.objects.get(pk=pk)
        comments = recipe.comments.all()
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.data['content']
            post = Comment.objects.create(content=content, user=request.user)
            recipe.comments.add(post)
            return render(request, 'app/recipe.html', {'recipe':recipe, 'comments':comments, 'form':CommentForm()})
    else:
        form = CommentForm()
    return render(request, 'app/recipe.html', {'recipe':recipe, 'comments':comments, 'form':form})

def upload_pic_at(request, pk):
    if request.method == 'POST':
        form2 = ImageUploadForm(request.POST, request.FILES)
        if form2.is_valid():
            m = Atelier.objects.get(pk=pk)
            m.picture = form2.cleaned_data['image']
            m.save()
        atelier = Atelier.objects.get(pk=pk)
        comments = atelier.comments.all()
        form = AtelierCommentForm(request.POST)
        if form.is_valid():
            content = form.data['content']
            post = AtelierComment.objects.create(content=content, user=request.user)
            atelier.comments.add(post)
            return render(request, 'app/atelier.html', {'atelier':atelier, 'comments':comments, 'form':AtelierCommentForm()})
    else:
        form = AtelierCommentForm()
    return render(request, 'app/atelier.html', {'atelier':atelier, 'comments':comments, 'form':form})


@login_required(login_url='/')
def recipe(request, pk):
    recipe = Recette.objects.get(pk=pk)
    comments = recipe.comments.all()
    try:
        notemoyenne = Notation.objects.filter(recette=recipe).aggregate(Sum('note')).values()[0]
    except ObjectDoesNotExist:
        notemoyenne = None
    if notemoyenne != None:
        notemoyenne = float(notemoyenne)  / float(Notation.objects.filter(recette=recipe).count())
    try:
        lastnote = Notation.objects.get(user=request.user, recette=recipe).note
    except ObjectDoesNotExist:
        lastnote = None
    if request.method == "POST":
        if 'note' in request.POST:
            noteform = NoteForm(request.POST)
            if noteform.is_valid():
                n = noteform.data['note']
                if lastnote == None:
                    notation = Notation.objects.create(user=request.user, recette=recipe, note=n)
                else:
                    notation = Notation.objects.get(user=request.user, recette=recipe)
                    notation.note = n
                    notation.save()
                lastnote = notation.note
                notemoyenne = float(Notation.objects.filter(recette=recipe).aggregate(Sum('note')).values()[0]) / float(Notation.objects.filter(recette=recipe).count())
        else :
            form = CommentForm(request.POST, request.FILES)
            if form.is_valid():
                content = form.data['content']
                post = Comment.objects.create(content=content, user=request.user)
                recipe.comments.add(post)
    return render(request, 'app/recipe.html', {'recipe':recipe, 'comments':comments, 'form':CommentForm(), 'note':NoteForm(), 'lastnote':lastnote, 'moyenne' : notemoyenne})

@login_required(login_url='/')
def commentDelete(request, pk, pkcomment):
    Comment.objects.get(id=pkcomment).delete()
    return redirect('recipe', pk)

@login_required(login_url='/')
def atelierNew(request):
    query = request.GET.get('q')
    if query:
        query_list = query.split()
        ateliers = Atelier.objects.filter(
            reduce(operator.and_, (Q(nom__icontains=q) for q in query_list)) |
            reduce(operator.and_, (Q(description__icontains=q) for q in query_list))).order_by('-date')[:24]
        mess = 'Atelier(s)'
        for q in query_list :
            for i in User.objects.all():
                if q.lower() in i.first_name.lower() or q.lower() in i.last_name.lower() :
                    ateliers = list(chain(ateliers, Atelier.objects.filter(chef=i)))
        users = User.objects.filter(
            reduce(operator.and_, (Q(first_name__icontains=q) for q in query_list)) |
            reduce(operator.and_, (Q(last_name__icontains=q) for q in query_list)))[:5]
        ateliers = sorted(set(ateliers))
    else :
        ateliers = Atelier.objects.order_by('-date')
        users = None
        mess = 'À venir'
    return render(request, 'app/listAteliers.html', {'ateliers':ateliers, 'users': users, 'message':mess})

@login_required(login_url='/')
def atelierPop(request):
    ateliers = Atelier.objects.reverse().annotate(commentnb=Count('comments')).order_by('-commentnb')[:24]
    return render(request, 'app/listAteliers.html', {'ateliers':ateliers, 'message':'Populaires'})

@login_required(login_url='/')
def recipeEntree(request):
    recipes = Recette.objects.filter(type='E')[:24]
    return render(request, 'app/listRecettes.html', {'recettes':recipes, 'message':'Les entrées'})

@login_required(login_url='/')
def recipePlat(request):
    recipes = Recette.objects.filter(type='P')[:24]
    return render(request, 'app/listRecettes.html', {'recettes':recipes, 'message':'Les plats'})

@login_required(login_url='/')
def recipeDessert(request):
    recipes = Recette.objects.filter(type='D')[:24]
    return render(request, 'app/listRecettes.html', {'recettes':recipes, 'message':'Les desserts'})

@login_required(login_url='/')
def recipeNew(request):
    query = request.GET.get('q')
    if query:
        query_list = query.split()
        recipes = Recette.objects.filter(
            reduce(operator.and_, (Q(nom__icontains=q) for q in query_list)) |
            reduce(operator.and_, (Q(recetteDetail__icontains=q) for q in query_list))).order_by('creation_date')[:24]
        mess = 'Recette(s)'
        for q in query_list :
            for i in User.objects.all():
                if q.lower() in i.first_name.lower() or q.lower() in i.last_name.lower() :
                   recipes = list(chain(recipes, Recette.objects.filter(user=i)))
        recipes = sorted(set(recipes))
        users = User.objects.filter(
            reduce(operator.and_, (Q(first_name__icontains=q) for q in query_list)) |
            reduce(operator.and_, (Q(last_name__icontains=q) for q in query_list)))[:5]
    else :
        users = None
        recipes = Recette.objects.order_by('creation_date')[:24]
        mess = 'Nouveautés'
    return render(request, 'app/listRecettes.html', {'recettes':recipes, 'users':users, 'message':mess})

@login_required(login_url='/')
def recipePop(request):
    recipes = Recette.objects.annotate(commentnb=Count('comments')).order_by('-commentnb')[:24]
    return render(request, 'app/listRecettes.html', {'recettes':recipes, 'message':'Populaires'})

# ATELIERS
@login_required(login_url='/')
def atelier(request, pk):
    atelier = Atelier.objects.get(pk=pk)
    comments = atelier.comments.all()
    inscrits = AtelierInscription.objects.filter(atelier=atelier)
    #content = request.POST.get('text_box')
    if request.method == "POST":
        form = AtelierCommentForm(request.POST)
        if form.is_valid():
            content = form.data['content']
            # recette = Recette.objects.get(pk=pk)
            post = AtelierComment.objects.create(content=content, user=request.user)
            atelier.comments.add(post)
            return render(request, 'app/atelier.html', {'atelier':atelier, 'comments':comments, 'form':AtelierCommentForm(), 'nbinscr': AtelierInscription.objects.filter(user=request.user).filter(atelier=atelier).count()})
    else:
        form = AtelierCommentForm()
    return render(request, 'app/atelier.html', {'atelier':atelier, 'comments':comments, 'form':form, 'inscrits':inscrits, 'nbinscr': AtelierInscription.objects.filter(user=request.user).filter(atelier=atelier).count()})

class AtelierCreate(CreateView):
    model = Atelier
    form_class = AtelierForm
    # fields = ['nom', 'chef', 'date', 'duration', 'prix', 'place', 'lieu', 'description', 'picture']
    def form_valid(self, form):
        atelier = form.save(commit=False)
        if not atelier.picture:
            atelier.picture = "/static/app/images/default.png"
        # atelier.date = form['date']
        atelier.restant = atelier.place
        atelier.save()
        return super(AtelierCreate, self).form_valid(form)





class AtelierUpdate(UpdateView):
    model = Atelier
    form_class = AtelierForm
    # fields = ['nom', 'chef', 'date', 'duration', 'prix', 'place', 'lieu', 'description', 'picture']
    def form_valid(self, form):
        atelier = form.save(commit=False)
        if atelier.picture:
            atelier.picture = "/static/app/images/default.png"
        atelier.save()
        return super(AtelierUpdate, self).form_valid(form)


class AtelierDelete(DeleteView):
    model = Atelier
    success_url = reverse_lazy('ateliers')

class UserCreate(CreateView):
    model = User

class UserprofileUpdate(UpdateView):
    model = User
    form_class = UserAdminForm
    second_form_class = UserForm

    template_name = 'app/user_form.html'
    # fields = ['nom', 'chef', 'date', 'duration', 'prix', 'place', 'lieu', 'description', 'picture']
    def get_context_data(self, **kwargs):
        context = super(UserprofileUpdate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context
    def form_valid(self, form):
        # user = form.save(commit=False)
        # user.save()
        if form.is_valid():
            userdata = form.save(commit=False)
            # used to set the password, but no longer necesarry
            userdata.save()
            #
            # messages.success(self.request, 'Settings saved successfully')
            # return HttpResponseRedirect(self.get_success_url())
        else:
             if form2.is_valid():
                 employeedata = form2.save(commit=False)
                 employeedata.user = userdata
                 employeedata.save()
             else:
                 return self.render_to_response(
                    self.get_context_data(form=form, form2=form2))
        return super(UserprofileUpdate, self).form_valid(form)

class UserUpdate(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'app/userprofile_form.html'
    # fields = ['nom', 'chef', 'date', 'duration', 'prix', 'place', 'lieu', 'description', 'picture']
    def form_valid(self, form):
        atelier = form.save(commit=False)
        atelier.save()
        return super(UserprofileUpdate, self).form_valid(form)



def userprofiledelete(request, pk):
    try:
        u = User.objects.get(pk=pk)
        u.delete()
    except User.DoesNotExist:
        return redirect('home')
    except Exception as e:
        return redirect('home')
    return redirect('home')

mc = 'Error during transaction'
@login_required(login_url='/')
def atelierInscription(request, pk):
    atelier = Atelier.objects.get(id=pk)

    #FIXME après paiement
    if request.method == "POST":
        nb = int(request.POST['place'])
        nom = str(request.POST['nom'])
        prenom = str(request.POST['prenom'])
        birth = str(request.POST['birth'])
        email = str(request.POST['email'])
        ville = str(request.POST['ville'])
        postal = int(request.POST['postal'])
        adresse = str(request.POST['adresse'])
        pays = str(request.POST['pays'])
        tel = request.POST['tel']
        telfixe = request.POST['telfixe']
        # inscription = AtelierInscription.objects.create(atelier=atelier, user=request.user, nbplace=nb)
        # inscription.save()
        global mc
        mc = str ('Votre commande à bien été enregistrée.\nL\'équipe Yakasserole vous attend le '
            + "{:%d/%m/%Y}".format(atelier.date)
            + '  à son atelier : ' + atelier.nom
            + ' !\nnombre de place(s) : ' + str(nb)
            + '\n\n Nom : ' + nom
            + '\n Prenom : ' + prenom
            + '\n Email : ' + email
            + '\n Ville : ' + ville
            + '\n Date de naissance : ' + "{:%d/%m/%Y}".format(datetime.strptime(birth, '%Y-%m-%d'))
            + '\n Code postal : ' + str(postal)
            + '\n Adresse : ' + adresse
            + '\n Pays : ' + pays
            + '\n Tel : ' + str(tel)
            + '\n Tel fixe : ' + str(telfixe)
            + '\n Prix : ' + str(atelier.prix * nb) + '€'
            + '\n\nL\'équipe Yakasserole.')
        return redirect('atelier-paiement', pk=pk, nb=nb)
    return render(request, 'app/ateliertotal.html', {'atelier':atelier,
                                                     'nbinscr': AtelierInscription.objects.filter(user=request.user).filter(atelier=atelier).count()})
    # if atelierInscription.objects.fiter(atelier=atelier, user=request.user).exists()
    #     # deja inscrit
    # else
    #     #

@login_required(login_url='/')
def atelierPaiement(request, pk, nb):
    atelier = Atelier.objects.get(pk=pk)
    total = int(nb)*atelier.prix
    totalpremium=0
    if User.objects.filter(groups__name='Client Premium', pk=request.user.pk).count() != 0:
        totalpremium = float(total)*0.9
    if request.method == "POST":
        inscription = AtelierInscription.objects.create(atelier=atelier, user=request.user, nbplace=nb)
        inscription.save()
        atelier.restant = atelier.restant - int(nb)
        atelier.save()
        global mc
        send_mail(
            'Récapitulatif de votre commande',
            mc,
            'yakasserolelespind@gmail.com',
            [request.user.email],
            fail_silently=False,
        )
        mc = 'Error during transaction'
        return redirect('atelier', pk)
    return render(request, 'app/atelierpaiement.html', {'nb':int(nb), 'total': total, 'atelier':atelier, 'nbinscr': AtelierInscription.objects.filter(user=request.user).filter(atelier=atelier).count(), 'totalpremium':totalpremium})

@login_required(login_url='/')
def premiumPaiement(request, prix):
    if request.method == "POST":
        nom = str(request.POST['nom'])
        prenom = str(request.POST['prenom'])
        birth = str(request.POST['birth'])
        email = str(request.POST['email'])
        ville = str(request.POST['ville'])
        postal = int(request.POST['postal'])
        adresse = str(request.POST['adresse'])
        pays = str(request.POST['pays'])
        tel = request.POST['tel']
        telfixe = request.POST['telfixe']
        mc = str('Votre commande à bien été enregistrée.\nL\'équipe Yakasserole est heureuse de vous compter parmi ses client Premium !'
            + '\n\n Nom : ' + nom
            + '\n Prenom : ' + prenom
            + '\n Email : ' + email
            + '\n Ville : ' + ville
            + '\n Date de naissance : ' + "{:%d/%m/%Y}".format(datetime.strptime(birth, '%Y-%m-%d'))
            + '\n Code postal : ' + str(postal)
            + '\n Adresse : ' + adresse
            + '\n Pays : ' + pays
            + '\n Tel : ' + str(tel)
            + '\n Tel fixe : ' + str(telfixe)
            + '\n Prix : ' + str(prix) + '€'
            + '\n\nL\'équipe Yakasserole.')
        send_mail(
            'Récapitulatif de votre commande',
            mc,
            'yakasserolelespind@gmail.com',
            [request.user.email],
            fail_silently=False,
        )

        user = User.objects.get(pk=request.user.pk)
        g = Group.objects.get(name='Client Premium')
        g.user_set.add(user)
        return redirect('home')
    return render(request, 'app/premium.html', {'prix' :prix})


@login_required(login_url='/')
def ateliercommentDelete(request, pk, pkcomment):
    AtelierComment.objects.get(id=pkcomment).delete()
    return redirect('atelier', pk)




@receiver(user_logged_in, dispatch_uid="unique")
def user_logged_in_(request, user, **kwargs):
    mymodel = request.user.profile
    mymodel.connections = F('connections') + 1
    mymodel.save()


@receiver(pre_delete, sender=Recette)
def cascade_delete_branch(sender, instance, **kwargs):
    for t in instance.comments.all():
        t.delete()


@receiver(pre_delete, sender=Atelier)
def cascade_delete_branch(sender, instance, **kwargs):

    for t in instance.comments.all():
        t.delete()

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="stats.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('stats')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Prénom', 'Nom', 'Email']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.all().values_list('first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    row_num += 2

    ws.write(row_num, 0, 'Utilisateurs', font_style)
    ws.write(row_num, 1 , str(User.objects.filter().count()), font_style)
    row_num += 1

    ws.write(row_num, 0, 'Inscriptions', font_style)
    ws.write(row_num, 1 , str(AtelierInscription.objects.filter().count()), font_style)
    row_num += 1

    ws.write(row_num, 0, 'Clients classiques', font_style)
    ws.write(row_num, 1 , str(User.objects.filter(groups__name=None).count()), font_style)
    row_num += 1

    ws.write(row_num, 0, 'Clients Premium', font_style)
    ws.write(row_num, 1 , str(User.objects.filter(groups__name='Client Premium').count()), font_style)
    row_num += 1

    ws.write(row_num, 0, 'Recettes', font_style)
    ws.write(row_num, 1 , str(Recette.objects.filter(user=request.user).count()), font_style)
    row_num += 1

    ws.write(row_num, 0, 'Ateliers', font_style)
    ws.write(row_num, 1 , str(Atelier.objects.filter().count()), font_style)
    row_num += 1

    ws.write(row_num, 0, 'Commentaires Recettes', font_style)
    ws.write(row_num, 1 , str(Comment.objects.filter().count()), font_style)
    row_num += 1

    ws.write(row_num, 0, 'Commentaires Ateliers', font_style)
    ws.write(row_num, 1 , str(AtelierComment.objects.filter().count()), font_style)
    wb.save(response)
    return response
