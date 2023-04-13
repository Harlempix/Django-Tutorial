from django.contrib import admin
from hello.models import Post
from hello.models import LogMessage
from hello.models import AllCats
from hello.models import PicSeries
from hello.models import SinglePic
from hello.models import SeriesCats

# Register your models here.
admin.site.register(Post)
admin.site.register(LogMessage)
admin.site.register(AllCats)
admin.site.register(PicSeries)
admin.site.register(SinglePic)
admin.site.register(SeriesCats)