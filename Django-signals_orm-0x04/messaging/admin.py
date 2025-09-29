from django.contrib import admin
from .models import Message, MessageHistory, Notification

admin.site.register(Message)
admin.site.register(Notification)
#add message history signal
admin.site.register(MessageHistory)

