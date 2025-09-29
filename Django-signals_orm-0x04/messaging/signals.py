from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Create a notification for the receiver when a new message is created.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before a Message is updated, save the old content to MessageHistory.
    """
    if instance.pk:  #check if message exists, not on new messages
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                #log previous content
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
                #mark the message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    When a user is deleted remove related messages, notifications,
    and message histories
    """
    #delete the messages
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    #delete the notifications
    Notification.objects.filter(user=instance).delete()

    MessageHistory.objects.filter(edited_by=instance).delete()