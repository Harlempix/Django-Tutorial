from django import forms
from hello.models import LogMessage
from .models import Post

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message",)   # NOTE: the trailing comma is required

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "cover",)