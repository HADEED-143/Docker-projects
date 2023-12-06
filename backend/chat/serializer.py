from rest_framework import serializers
from .models import Message
from django.contrib.auth import get_user_model
from users.serializer import CustomUserSerializer
User = get_user_model()




class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(read_only=True)
    receiver = CustomUserSerializer(read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), source='sender')
    receiver_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), source='receiver')

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'sender_id', 'receiver_id',
                  'message', 'timestamp', 'is_read')
        read_only_fields = ('id', 'timestamp', 'is_read', 'sender', 'receiver')
