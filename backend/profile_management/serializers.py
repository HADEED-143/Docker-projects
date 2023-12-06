from rest_framework import serializers
from .models import WorkerSkill, Experience, Education

from users.serializer import CustomUserSerializer

class WorkerSkillSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only = True)
    class Meta:
        model = WorkerSkill
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

# class WorkerSerializer(serializers.ModelSerializer):
#     skills = SkillSerializer(many=True)
#     class Meta:
#         model = Worker
#         fields = '__all__'
