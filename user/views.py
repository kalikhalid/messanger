from django.shortcuts import render
from .models import User, Message
from django.http import HttpResponse, HttpRequest
# Create your views here.

def req(request: HttpRequest):
    return render(request, "user/index.html")

def get_send_message_page(request: HttpRequest):
    if request.method == "POST":
        user, created = User.objects.get_or_create(username=request.user.username)
        msg = Message.objects.create(text=request.POST.get("message_text"), user=user)
        user.save()
        msg.save()
    return render(request, "user/post_form.html")
