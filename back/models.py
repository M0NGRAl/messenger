from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True, blank=True)  # Поле теперь необязательное
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='direct_messages', null=True, blank=True)  # Для личных сообщений
    text = models.TextField()

    def __str__(self):
        return f'{self.user}: {self.text}'