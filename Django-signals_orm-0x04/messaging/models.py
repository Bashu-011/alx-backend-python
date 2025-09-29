from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    #for threading messages
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE
    )

    objects = models.Manager()  
    unread = UnreadMessagesManager()  

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:30]}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - Message {self.message.id}"
    
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='edited_histories')

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        #get unread messages
        return self.filter(receiver=user, read=False).only("id", "sender", "content", "timestamp")


