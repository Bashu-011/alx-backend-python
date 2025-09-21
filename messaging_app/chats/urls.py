# messaging_app/chats/urls.py

from django.urls import path, include
from messaging_app.chats import admin
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

#creating router and registering views
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

#api routes are assigned automatically
urlpatterns = [
    path('', include(router.urls)),  
    path('admin/', admin.site.urls),
    path('api/', include('messaging_app.chats.urls')), 
]
