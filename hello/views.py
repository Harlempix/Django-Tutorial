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
from hello.models import LogMessage
from hello.models import Post
from django.views.generic import ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from pathlib import Path
from django.http import HttpResponseRedirect


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
    post_obj=Post.objects.get(pk=post_id)
    post_obj.create_thumbnail()
    return HttpResponseRedirect('/post-list')

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

def new_image(request):
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
