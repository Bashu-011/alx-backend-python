from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Return unread messages for a specific user
    """
    def unread_for_user(self, user):
        if user is None:
            return self.none()
        return self.get_queryset().filter(receiver=user, read=False)
