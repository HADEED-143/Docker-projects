from rest_framework import serializers
from django.contrib.auth import password_validation
from django.contrib.auth.models import Group
from .models import CustomUser, Worker, Client
from django.contrib.gis.geos import Point
from django.contrib.auth.password_validation import validate_password

from PIL import Image

from django.utils.html import escape
from django.contrib.auth.hashers import make_password


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'age', 'gender',
            'city', 'phone_number', 'bio',
            'profile_picture', 'address', 'date_joined',
            'email', 'id', 'role', 'is_active', 'location',
        )


class UserRegistrationSerializer(serializers.ModelSerializer):

    # Add the profile_picture field for handling the profile picture upload
    profile_picture = serializers.ImageField(allow_null=True, required=False)
    confirmPassword = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'age', 'gender', 'role',
                  'city', 'phone_number', 'profile_picture', 'bio', 'date_joined', 'address', 'confirmPassword', 'location')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Remove confirmPassword from validated_data before creating the instance
        validated_data.pop('confirmPassword', None)
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])

        # Create the user instance
        user = super().create(validated_data)

        # Assign the user to the group corresponding to their role choice
        role = validated_data.get('role')
        if role:
            try:
                group = Group.objects.get(name=role)
            except Group.DoesNotExist:
                group = Group.objects.create(name=role)
            user.groups.add(group)

        location = Point(float(self.context['request'].data['longitude']), float(
            self.context['request'].data['latitude']))
        # If the user's role is 'worker', create a Worker instance for this user
        if role == 'worker':
            Worker.objects.create(
                user=user, wage=0, hourly_rate=0, rating=0, location=location)
        elif role == 'client':
            Client.objects.create(
                user=user, location=location)
        return user

    def validate(self, data):
        password = data.get('password')
        confirmPassword = data.get('confirmPassword')

        # Check if the passwords match
        if password != confirmPassword:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def validate_password(self, value):
        # Validate password length
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters long.")

        # Use Django's built-in password validation
        validate_password(value)

        return value

    def validate_first_name(self, value):
        # Sanitize first_name
        return escape(value.strip())

    def validate_last_name(self, value):
        # Sanitize last_name
        return escape(value.strip())

    def validate_age(self, value):
        # Validate age (example: between 13 and 100)
        if value < 13 or value > 100:
            raise serializers.ValidationError(
                "Age must be between 13 and 100.")
        return value

    def validate_phone_number(self, value):
        # Validate phone number (example: must be 11 digits long)
        if len(value) != 11 or not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must be 11 digits long.")
        return value

    def validate_profile_picture(self, value):

        # Validate that the uploaded file is an image.
        # Check if the value is None (no file provided)
        if not value:
            return value

        # Open and validate the image
        try:
            img = Image.open(value)
            img.verify()  # Verify the image file
        except Exception as e:
            raise serializers.ValidationError("Invalid image file format.")

        # Check the image format
        if not img.format.lower() in ['jpeg', 'jpg', 'png', 'gif']:
            raise serializers.ValidationError(
                "Unsupported image format. Please use JPEG, PNG, or GIF.")

        return value


class WorkerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Worker
        fields = '__all__'
