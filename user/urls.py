from django.contrib import admin
from django.urls import path, include
from user.views import req, get_send_message_page
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("", req, name="chat"),
    path("send-get/", get_send_message_page, name="get_message"),
    path("login/", LoginView.as_view(template_name="user/login.html"), name='login'),
]
