from django import forms
from hello.models import LogMessage
from .models import Post
from .models import AllCats
from .models import PicSeries

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message",)   # NOTE: the trailing comma is required

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "cover",)

#-------------------------- Multi-Pic-Handling ------------------------------
class SysMessageForm(forms.Form):
    dummy = forms.CharField(label="Sollte nie zu sehen sein", max_length=100)

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

class f_PicSeries_c(forms.Form):
    choices = tuple(AllCats.objects.all().values_list("cat", "description"))
    title = forms.CharField(max_length=80)
    description = forms.CharField()
    catPrime = forms.ChoiceField(choices=choices)
    dateCaptured = forms.DateTimeField()
    file_field = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"multiple": True})
    )

class f_PicSeries_u(forms.Form):
    choices = tuple(AllCats.objects.all().values_list("cat", "description"))
    title = forms.CharField(max_length=80)
    owner = forms.CharField(required=False, disabled=True)
    description = forms.CharField()
    catPrime = forms.ChoiceField(choices=choices)
    dateCaptured = forms.DateTimeField()
    file_field = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"multiple": True})
    )


