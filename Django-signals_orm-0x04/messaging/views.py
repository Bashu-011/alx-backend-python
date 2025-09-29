from mailbox import Message
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    Allow an authenticated user to delete their account
    """
    user = request.user
    username = user.username
    user.delete()
    return Response(
        {"details": f"User '{username}' and related data deleted."},
        status=status.HTTP_204_NO_CONTENT,
    )


def conversation_messages(request, conversation_id):
    """
    Get messages in a conversation with proper queries
    """
    messages = (
        Message.objects.filter(conversation_id=conversation_id, parent_message__isnull=True)
        .select_related("sender", "receiver")      
        .prefetch_related("replies")               # optimize replies fetching
    )

    data = []
    for msg in messages:
        data.append(serialize_message(msg))

    return JsonResponse(data, safe=False)


def serialize_message(message):
    """
    Serialize a message and its ralated replies
    """
    return {
        "id": message.id,
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "timestamp": message.timestamp,
        "replies": [serialize_message(reply) for reply in message.replies.all()],
    }

@login_required
def inbox(request):
    """
    Display only unread messages for the logged-in user.
    """
    unread_qs = Message.unread.unread_for_user(request.user).select_related('sender').only('id', 'sender', 'content', 'timestamp')
    return render(request, 'messaging/inbox.html', {'unread_messages': unread_qs})