from django.shortcuts import render
from .models import User, Message, Chat
from django.http import HttpResponse, HttpRequest
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.db.models import Q 

class MessageCreateView(CreateView):
    model = Message
    fields = "text", "receiver", "chat_id"
    template_name = "user/post_form.html"
    success_url = reverse_lazy("get_message")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response
    
class ChatCreateView(CreateView):
    model = Chat
    fields = "name", "users",
    template_name = "user/chat_form.html"
    success_url = reverse_lazy("chat")


def req(request: HttpRequest):
    return render(request, "user/index.html")

def get_send_message_page(request: HttpRequest):
    if request.method == "POST":
        receiver = User.objects.get(username=request.POST.get("username"))
        chat_name = Chat.objects.get(name=request.POST.get("name"))
        user, created = User.objects.get_or_create(username=request.user.username)
        if receiver:
            msg = Message.objects.create(text=request.POST.get("message_text"), user=user, receiver=receiver)
            user.save()
            msg.save()
        if chat:
            chat = Chat.objects.get(name=chat_name)
            msg = Message.objects.create(text=request.POST.get("message_text"), user=user, chat_id=chat)
            user.save()
            chat.save()
            msg.save()
    return render(request, "user/post_form.html")

def get_messages(request: HttpRequest):
    user_chats = User.objects.get(username=request.user.username).chats.all()
    all_messges = Message.objects.filter(Q(receiver=request.user.pk) | Q(chat_id__in=user_chats)).all()
    if request.method == "POST":
        for i in all_messges:
            if not i.is_read:
                i.is_read = True
                i.save()
    read_messages = [ i for i in all_messges if i.is_read]
    unread = [i for i in all_messges if not i.is_read]
    context = {
        "unread": unread,
        "read": read_messages,
        "msgs": all_messges,
    }    
    return render(request, "user/received.html", context=context)


