from django import forms
from hello.models import LogMessage
from .models import Post
from .models import AllCats

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message",)   # NOTE: the trailing comma is required

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "cover",)

#-------------------------- Multi-Pic-Handling ------------------------------
class AllCatsForm(forms.ModelForm):
    class Meta:
        model = AllCats
        fields = ("cat", "description",)
        labels = {
            "cat": "Kategorie",
        }
        help_texts = {
            "cat": "Eine kurze eindeutige Bezeichnung",
        }
        error_messages = {
            "cat": {
                "required": "Die Kategorie muss ausgefüllt werden",
                "unique": "Diese Kategorie existiert bereits"
            },
        }