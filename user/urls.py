from django.contrib import admin
from django.urls import path, include
from user.views import req, get_send_message_page, get_messages, MessageCreateView, ChatCreateView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("", req, name="chat"),
    path("send-get/", MessageCreateView.as_view(), name="get_message"),
    path("messages/", get_messages, name="messages"),
    path("login/", LoginView.as_view(template_name="user/login.html"), name='login'),
    path("create-chat/", ChatCreateView.as_view(), name="create_chat"),
]
