from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from .models import Message
from .serializer import MessageSerializer

from .pusher import pusher_client

# Create your views here.


class MessageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        sender_id = self.kwargs['sender_id']
        receiver_id = self.kwargs['receiver_id']

        messages = Message.objects.filter(sender_id=sender_id, receiver_id=receiver_id) | Message.objects.filter(
            sender_id=receiver_id, receiver_id=sender_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            pusher_client.trigger(
                'chat', 'message', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMessagesAPIView(APIView):

    # return list of messages for a user in reverse order
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        messages = Message.objects.filter(sender_id=user_id) | Message.objects.filter(
            receiver_id=user_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)