from rest_framework.permissions import BasePermission

# messaging_app/chats/permissions.py
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Access  for only the owner of the message
    or participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'sender'): 
            return obj.sender == request.user
        elif hasattr(obj, 'participants'):  
            return request.user in obj.participants.all()
        return False
