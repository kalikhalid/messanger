from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    users = models.ManyToManyField(User, related_name="chats")
    name = models.CharField(blank=True, max_length=50)

    def __str__(self) -> str:
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sended_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    text = models.TextField(blank=False)
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, related_name='received_messages', null=True)
    chat_id = models.ForeignKey(Chat, blank=True, null=True, on_delete=models.CASCADE)