from rest_framework import viewsets, permissions
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, UserSerializer, UserMessageSerializer
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

def index(request):
    return render(request, 'index.html')

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        chat = serializer.save()  # Сохранить чат
        chat.users.add(self.request.user)  # Добавить текущего пользователя в чат

    def get_queryset(self):
        # Показывать только чаты, в которых участвует текущий пользователь
        return Chat.objects.filter(users=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            raise NotFound("Чат не найден.")

        # Возвращаем только сообщения, связанные с этим чатом
        return Message.objects.filter(chat=chat)

    def perform_create(self, serializer):
        chat_id = self.kwargs.get('chat_id')
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            raise NotFound("Чат не найден.")

        # Создаем сообщение, привязывая его к чату и пользователю
        serializer.save(chat=chat, user=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Можно добавить защиту для UserViewSet

class UserMessageViewSet(viewsets.ModelViewSet):
    serializer_class = UserMessageSerializer
    permission_classes = [permissions.IsAuthenticated]  # Защита для UserMessageViewSet

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id is not None:
            return Message.objects.filter(recipient_id=user_id)  # Предполагается, что recipient - это поле для ЛС
        return Message.objects.none()

    def create(self, request, user_id=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(recipient=user, user=request.user)  # Убедитесь, что сохраняете и текущего пользователя
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Если сериализатор не валиден, возвращаем ошибки
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
