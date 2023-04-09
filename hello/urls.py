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
]
