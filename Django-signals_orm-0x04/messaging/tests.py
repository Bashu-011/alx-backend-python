from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class MessagingSignalTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="password123")
        self.receiver = User.objects.create_user(username="bob", password="password123")

    def test_notification_created_on_new_message(self):
        #create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello John DOe!"
        )

        #check if notification has been created
        notifications = Notification.objects.filter(user=self.receiver, message=message)
        self.assertEqual(notifications.count(), 1)
