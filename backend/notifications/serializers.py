from .models import Notifications
from rest_framework import serializers
from users.serializer import CustomUserSerializer
from users.models import CustomUser

class NotificationsSerializer(serializers.ModelSerializer):
    receiver = CustomUserSerializer(read_only=True)
    receiver_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=CustomUser.objects.all(), source='receiver')
    class Meta:
        model = Notifications
        fields = '__all__'
        read_only_fields = ['id', 'reciever', 'created_at', 'updated_at']
        