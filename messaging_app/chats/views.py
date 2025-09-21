from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.decorators import action

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    #creating a conversation
    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        """
        Create new conversation. The request should include a list of participant ids
        """
        participants = request.data.get('participants')
        if not participants or len(participants) < 2:
            return Response({"error": "A conversation must have at least two participants."}, status=status.HTTP_400_BAD_REQUEST)

        # Create conversation
        conversation = Conversation.objects.create()

        #add participants to convo
        for user_id in participants:
            try:
                user = User.objects.get(id = user_id)
                conversation.participants.add(user)
            except User.DoesNotExist:
                return Response({"error": f"User with id {user_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        conversation.save()

        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    #send message to an existing convo
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        The request should include the message body and sender ID
        """
        try:
            conversation = Conversation.objects.get(id=pk)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        sender_id = request.data.get('sender_id')
        message_body = request.data.get('message_body')

        if not sender_id or not message_body:
            return Response({"error": "Both sender ID and message body are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sender = User.objects.get(id=sender_id)
        except User.DoesNotExist:
            return Response({"error": "Sender not found."}, status=status.HTTP_404_NOT_FOUND)

        #create message and add to convo
        message = Message.objects.create(sender=sender, message_body=message_body, conversation=conversation)

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
