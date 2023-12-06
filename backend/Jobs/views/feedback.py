from ..models import Feedback
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from ..serializers import FeedbackSerializer
from users.models import CustomUser
from Jobs.Models.job import Job


class FeedbackList(generics.ListCreateAPIView):
    queryset = Feedback.objects.select_related(
        'job', 'feedback_sender', 'feedback_receiver').all()
    serializer_class = FeedbackSerializer
    filterset_fields = ['job__title', 'rating', 'comment']
    search_fields = ['job__title', 'rating', 'comment']

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permissions() for permissions in permission_classes]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        feedback_receiver_id = request.data.get('feedback_receiver_id')
        feedback_sender_id = request.data.get('feedback_sender_id')
        job_id = request.data.get('job_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment')

        if not user:
            return Response({'response': "You don't have permission to create a feedback."})
        if not feedback_receiver_id:
            return Response({'response': "Please provide a feedback receiver."})
        if not feedback_sender_id:
            return Response({'response': "Please provide a feedback sender."})
        if not job_id:
            return Response({'response': "Please provide a job."})
        if not rating:
            return Response({'response': "Please provide a rating."})
        if not comment:
            return Response({'response': "Please provide a comment."})
        if not CustomUser.objects.filter(id=feedback_receiver_id).exists():
            return Response({'response': "Feedback receiver not found."})
        if not CustomUser.objects.filter(id=feedback_sender_id).exists():
            return Response({'response': "Feedback sender not found."})
        if not Job.objects.filter(id=job_id).exists():
            return Response({'response': "Job not found."})
        if not (1 <= int(rating) <= 5):
            return Response({'response': "Rating must be between 1 and 5."})

        feedback = Feedback.objects.create(
            feedback_receiver_id=feedback_receiver_id,
            feedback_sender_id=feedback_sender_id,
            job_id=job_id,
            rating=rating,
            comment=comment
        )
        feedback.save()
        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FeedbackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.select_related(
        'job', 'sender', 'receiver').all()
    serializer_class = FeedbackSerializer
    filterset_fields = ['job__title', 'rating', 'comment']
    search_fields = ['job__title', 'rating', 'comment']

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permissions() for permissions in permission_classes]
