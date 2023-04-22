from django.urls import path, include

from hello import views
from hello.models import LogMessage
from hello.models import Post


home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="hello/home.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("post-add/", views.new_image, name="post-add"),  # new
    path("hello/<name>", views.hello_there, name="hello_there"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("log/", views.log_message, name="log"),
    path("accounts/login/", views.log_message, name="login"),
    path("accounts/logout/", views.log_message, name="logout"),
    path("create_thumbnail/", views.create_thumbnail, name="create_thumbnail"),
#-------------------------------- Multi-Pic-Handling-------------------------------------------
    path("SysMessage/", views.SysMessage, name="hello_SysMessage"),
    path("List_AllCats/", views.List_AllCats.as_view(), name="hello_ListAllCats"),
    path("Neu_AllCats/", views.Neu_AllCats, name="hello_NeuAllCats"),
    path("Edit_AllCats/<str:cat>", views.Edit_AllCats, name="hello_EditAllCats"),
    path("PicSeries/List", views.v_PicSeries_List.as_view(), name="hello_PicSeries_List"),
    path("PicSeries/Create", views.v_PicSeries_c, name="hello_PicSeries_Create"),
    path("PicSeries/Update/<int:PicSeriesId>", views.v_PicSeries_u, name="hello_PicSeries_Update"),
    path("PicSeries/SetHero", views.v_SetHero, name="hello_v_SetHero"),
    path("PicSeries/DeleteSinglePic", views.v_SinglePic_d, name="hello_v_SinglePic_d"),
]

