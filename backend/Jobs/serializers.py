from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework.serializers import PrimaryKeyRelatedField
from django.contrib.auth import get_user_model
from users.serializer import CustomUserSerializer, WorkerSerializer
from users.models import Worker

CustomUser = get_user_model()


class JobCategorySerializer(ModelSerializer):
    class Meta:
        model = JobCategory
        fields = '__all__'
        read_only_fields = ['id']


class JobImagesSerializer(ModelSerializer):
    class Meta:
        model = JobImages
        fields = '__all__'
        read_only_fields = ['id', 'job']


class JobSerializer(ModelSerializer):
    category = JobCategorySerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)
    category_id = PrimaryKeyRelatedField(
        write_only=True, queryset=JobCategory.objects.all(), source='category')
    worker = WorkerSerializer(read_only=True)
    images = JobImagesSerializer(many=True, read_only=True)
    # worker id can be null as well
    worker_id = PrimaryKeyRelatedField(
        write_only=True, queryset=Worker.objects.all(), source='worker', required=False)

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['id', 'user', 'category']
        extra_kwargs = {
            'labors_required': {'max_value': 6, 'min_value': 1}
        }


class JobImageSerializer(ModelSerializer):
    class Meta:
        model = JobImages
        fields = '__all__'
        read_only_fields = ['id', 'job', ]


class JobBidSerializer(ModelSerializer):
    worker = WorkerSerializer(read_only=True)
    worker_id = PrimaryKeyRelatedField(write_only=True, queryset=Worker.objects.all(
    ), source='worker', required=True)  # worker id can be null as well
    job = JobSerializer(read_only=True)
    job_id = PrimaryKeyRelatedField(
        write_only=True, queryset=Job.objects.all(), source='job', required=True)

    class Meta:
        model = JobBid
        fields = '__all__'


class FeedbackSerializer(ModelSerializer):
    job = JobSerializer(read_only=True)
    job_id = PrimaryKeyRelatedField(
        write_only=True, queryset=Job.objects.all(), source='job')
    feedback_receiver = CustomUserSerializer(read_only=True)
    feedback_receiver_id = PrimaryKeyRelatedField(
        write_only=True, queryset=CustomUser.objects.all(), source='worker')
    feedback_sender = CustomUserSerializer(read_only=True)
    feedback_sender_id = PrimaryKeyRelatedField(
        write_only=True, queryset=CustomUser.objects.all(), source='user')

    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['id', 'job', 'reciever', 'sender', ]
        required_fields = ('rating', 'comment', 'job_id',
                           'receiver_id', 'sender_id', )
