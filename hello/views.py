import re
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from hello.forms import LogMessageForm
from hello.forms import PostForm
from hello.forms import SysMessageForm
from hello.models import LogMessage
from hello.models import Post
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from pathlib import Path
from django.http import HttpResponseRedirect
from hello.models import AllCats
from hello.models import PicSeries
from hello.models import SinglePic
from hello.models import SeriesCats
from hello.forms import AllCatsForm
from django.shortcuts import get_object_or_404
from hello.forms import f_PicSeries_c
from hello.forms import f_PicSeries_u

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

class PostListView(ListView):
    model = Post
    template_name = "hello/post-list.html"
    ordering = ['-id']
    paginate_by = 10

class CreatePostView(CreateView):  # new Post
    model = Post
    form_class = PostForm
    template_name = "hello/post-add.html"
    success_url = reverse_lazy("post-list")

def about(request):
    return render(request, "hello/about.html")

def contact(request):
    return render(request, "hello/contact.html")

def hello_there(request, name):
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def create_thumbnail(request):
    post_id=request.GET.get('post_id')
    page=request.GET.get('page')
    url=request.GET.get('url')

    post_obj=Post.objects.get(pk=post_id)
    post_obj.create_thumbnail()
    return HttpResponseRedirect(url)

def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "hello/log_message.html", {"form": form})

#####################################################################################
def new_image(request): #vvvvvvvvvvvvvvvvvvvvvvvvvvv Ein neues Bild in die Datenbank
    form = PostForm(request.POST, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            newPost = form.save(commit=False)
            newPost.owner = request.user.get_username()
            newPost.save()
            newPost.create_thumbnail()
            return redirect("post-list")
    else:
        return render(request, "hello/post-add.html", {"form": form})
    return redirect("post-list")
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#####################################################################################
#------------------------------- Multi-Pic-Handling -----------------------------
class List_AllCats(ListView):
    """Renders a page, with a list of all Cats."""
    model = AllCats
    template_name = "hello/List_AllCats.html"
    ordering = ['cat']


def Neu_AllCats(request):
    form = AllCatsForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            newCat = form.save(commit=False)
            newCat.save()
            return redirect("hello_ListAllCats")
        else:
            return render(request, "hello/AllCats.html", {"form": form})
    else:
        return render(request, "hello/AllCats.html", {"form": form})

####################################################################################################
class Try_Edit_AllCats(UpdateView):##### 404-Handling Funktioniert leider nicht
    model=AllCats
    fields="__all__"
    template_name='hello/AllCats.html'
    success_url='/List_AllCats/'
    def get_object(self):
        if self.request.user.is_authenticated: # Update nur für angemeldete User
            try: # Für den Fall, dass die Seite manuell mit falschen Parameter aufgerufen wurde
                return AllCats.objects.get(cat=self.kwargs['cat'])
            except AllCats.DoesNotExist:
                raise Http404("Die angeforderte Kategorie existiert nicht")
        else:
            raise Http404("Diese Funktion steht nur angemeldeten Usern zur Verfügung")
####################################################################################################
def SysMessage( request):
    form = SysMessage(request.POST or None)
    return render(request, "hello/sys_message.html", {'form' : form})

####################################################################################################

def Edit_AllCats( request, cat):
    context = {}
    if request.user.is_authenticated: # Update nur für angemeldete User
        try: # Für den Fall, dass die Seite manuell mit falschen Parameter aufgerufen wurde
            iCat = AllCats.objects.get(cat=cat)
        except AllCats.DoesNotExist: # Aufruf mit ungültiger Kategorie
#            form = SysMessageForm(request.POST or None)
#            context['form'] = form
            context['MsgLogin'] = "Fehler: Die Kategorie " + cat + " ist nicht im System"
            return render(request, "hello/sys_message.html", context)
        form = AllCatsForm(request.POST or None, instance = iCat)
        if form.is_valid():
            form.save()
            return redirect("hello_ListAllCats")
        else:
            context['form'] = form
            return render(request, "hello/AllCats.html", context)
    else: # Irgendwie hat ein unangemeldeter Benutzer diese Seite direkt aufgerufen
#        form = SysMessageForm(request.POST or None)
#        context['form'] = form
        context['MsgLogout'] = "Fehler: Diese Funktion steht nur angemeldeten Benutzern zur Verfügung"
        return render(request, "hello/sys_message.html", context)

####################################################################################################
def v_PicSeries_c(request):
    form = f_PicSeries_c(request.POST, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            newPicSeries = PicSeries()
            newPicSeries.title = form.cleaned_data["title"]
            newPicSeries.description = form.cleaned_data["description"]
            newPicSeries.owner = request.user.get_username()
            newPicSeries.dateCaptured = form.cleaned_data["dateCaptured"]
            newPicSeries.dateCreated = datetime.now()
            newPicSeries.dateModified = datetime.now()
            catPrime = AllCats.objects.get(cat = form.cleaned_data["catPrime"])
            newPicSeries.catPrime = catPrime
            newPicSeries.save()

            images = request.FILES.getlist("file_field")
            thn = "True"
            for i in images:
                newPic = SinglePic(series=newPicSeries)
                newPic.bigPic = i
                newPic.save()
                newPic.create_thumbnail()
                if thn == "True":
                    newPicSeries.hero = newPic.thumbnail
                    newPicSeries.save()
                    thn = "False"
            return redirect("hello_PicSeries_List")
        else:
            return render(request, "hello/t_PicSeries_c.html", {"form": form})
    else:
        return render(request, "hello/t_PicSeries_c.html", {"form": form})

####################################################################################################
class v_PicSeries_List(ListView):
    """Renders a page, with a list of all Cats."""
    model = PicSeries
    template_name = "hello/t_PicSeries_List.html"
    ordering = ['-dateCreated']

####################################################################################################
def v_PicSeries_u(request, PicSeriesId):
    context = {}
    if request.user.is_authenticated: # Update nur für angemeldete User
        try: # Für den Fall, dass die Seite manuell mit falschen Parameter aufgerufen wurde
            iPicSeries = PicSeries.objects.get(pk=PicSeriesId)
        except PicSeries.DoesNotExist: # Aufruf mit ungültiger Kategorie
            context['MsgLogin'] = "Fehler: Die Bildserie " + PicSeriesId + " ist nicht im System"
            return render(request, "hello/sys_message.html", context)
        form = f_PicSeries_u(request.POST, request.FILES or None)
        if request.method == "POST":
            if form.is_valid(): # Werte aus Form übernehmen
                iPicSeries.title = form.cleaned_data["title"]
                iPicSeries.description = form.cleaned_data["description"]
                iPicSeries.catPrime = AllCats.objects.get(cat = form.cleaned_data["catPrime"])
                iPicSeries.dateCaptured = form.cleaned_data["dateCaptured"]
                iPicSeries.dateModified = datetime.now()
                iPicSeries.save()
                images = request.FILES.getlist("file_field")
                for i in images:
                    newPic = SinglePic(series=iPicSeries)
                    newPic.bigPic = i
                    newPic.save()
                    newPic.create_thumbnail()
                return redirect("hello_PicSeries_List")
            else:
                context['MsgLogout'] = "Fehler: Hier ist was schiefgelaufen. Bitte noch einmal probieren oder Sysadmin benachrichtigen"
                return render(request, "hello/sys_message.html", context)
        else: # Form mit Werten füllen und anzeigen
            context = {}
            singlePics = SinglePic.objects.filter(series=iPicSeries.pk)
            initial_dict = {
                "title" : iPicSeries.title,
                "description" : iPicSeries.description,
                "catPrime" : iPicSeries.catPrime.cat,
                "dateCaptured" : iPicSeries.dateCaptured,
                "owner" : iPicSeries.owner,
                "hero" : iPicSeries.hero
            }
            form = f_PicSeries_u(initial = initial_dict)
            context['form'] = form
            context['singlePics'] = singlePics
            context['hero'] = iPicSeries.hero
            context['picSeriesId'] = iPicSeries.pk

            return render(request, "hello/t_PicSeries_u.html", context)
    else:
        context['MsgLogout'] = "Fehler: Diese Funktion steht nur angemeldeten Benutzern zur Verfügung"
        return render(request, "hello/sys_message.html", context)

####################################################################################################

def v_SetHero(request):
    heroId=request.GET.get('heroId')
    picSeriesId=request.GET.get('PicSeriesId')
    url=request.GET.get('url')

    iSinglePic = SinglePic.objects.get(pk=heroId)
    iPicSeries = PicSeries.objects.get(pk=picSeriesId)
    iPicSeries.hero = iSinglePic.thumbnail
    iPicSeries.save()
    return HttpResponseRedirect(url)

####################################################################################################

def v_SinglePic_d(request):
    singlePicId=request.GET.get('singlePicId')
    url=request.GET.get('url')

    iSinglePic = SinglePic.objects.get(pk=singlePicId)
    iSinglePic.delete()
    return HttpResponseRedirect(url)