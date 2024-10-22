from rest_framework import serializers
from .models import Chat, Message
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat', 'user', 'text']  # Добавим timestamp, если нужно

class ChatSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Chat
        fields = ['id', 'name', 'users']

class UserMessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'user', 'recipient', 'text']  # Убедитесь, что recipient тоже включен, если это необходимо

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user  # Автоматически присваиваем текущего пользователя
        return super().create(validated_data)