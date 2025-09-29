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
