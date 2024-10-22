from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, MessageViewSet, UserViewSet, UserMessageViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet, basename='messages')
router.register(r'usermessages', UserMessageViewSet, basename='usermessages')

urlpatterns = [
    path('', include(router.urls)),
    path('chats/<int:chat_id>/messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='chat-messages'),
    path('users/<int:user_id>/messages/', UserMessageViewSet.as_view({'post': 'create', 'get': 'list'}), name='send-user-message'),
]