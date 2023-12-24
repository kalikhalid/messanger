from django.shortcuts import render
from .models import User, Message
from django.http import HttpResponse, HttpRequest
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class MessageCreateView(CreateView):
    model = Message
    fields = "text", "receiver"
    template_name = "user/post_form.html"
    success_url = reverse_lazy("get_message")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response
    


def req(request: HttpRequest):
    return render(request, "user/index.html")

def get_send_message_page(request: HttpRequest):
    if request.method == "POST":
        receiver = User.objects.get(username=request.POST.get("username"))
        if receiver:
            user, created = User.objects.get_or_create(username=request.user.username)
            msg = Message.objects.create(text=request.POST.get("message_text"), user=user, receiver=receiver)
            user.save()
            msg.save()
    return render(request, "user/post_form.html")

def get_messages(request: HttpRequest):
        
    all_messges = Message.objects.filter(receiver=request.user.pk).all()
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
