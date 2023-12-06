from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions

from .models import Notifications
from .serializers import NotificationsSerializer

# Create your views here.


class NotificationsList(generics.ListCreateAPIView):
    serializer_class = NotificationsSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user:
            return Notifications.objects.filter(reciever=user.id)
        return Notifications.objects.none()


class NotificationsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
