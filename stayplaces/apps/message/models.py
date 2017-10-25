from __future__ import unicode_literals
from django.db import models
from ..users.models import User, Host
from ..locations.models import Place

# Create your models here.
class Conversation(models.Model):
    host =  models.ForeignKey(User, related_name="host_conversations")
    guest =  models.ForeignKey(User, related_name="guest_conversations")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Message(models.Model):
    content = models.CharField(max_length=500, blank=True)
    host = models.ForeignKey(User,related_name="host_messages")
    guest = models.ForeignKey(User, related_name="guest_messages")
    sender_id = models.IntegerField(blank=False, null=False)
    conversation = models.ForeignKey(Conversation, blank=False, null=False, related_name="messages")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    ordering = ["-created_at"]

