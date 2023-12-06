from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import fromstr
from django.contrib.postgres.fields import ArrayField
from django.db.models import Q

from django.utils import timezone
from utils.helper import GENDER_CHOICES, ROLE_CHOICES


from django.contrib.gis.db import models


class CustomUserManager(BaseUserManager):

    # use email, phone_number field as username field
    def get_by_natural_key(self, username: str | None) -> any:
        return self.get(Q(email=username) | Q(phone_number=username))

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "superuser")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("role") != "superuser":
            raise ValueError("Superuser must have role=superuser.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    # Add the 'role' field with choices
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True)
    city = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(
        max_length=11, null=True, unique=True)  # Add the phone_number field

    address = models.CharField(max_length=255, null=True)
    bio = models.TextField(null=True)

    location = models.PointField(null=True, blank=True)

    # stores date and the time when an instance of the model is created.
    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name",
                       "role", "gender"]  # Add other required fields

    def __str__(self):
        return self.email


class Worker(models.Model):
    skills = ArrayField(models.CharField(
        max_length=255), blank=True, null=True)
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='worker')
    wage = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    hourly_rate = models.DecimalField(
        max_digits=6, decimal_places=2, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    is_available = models.BooleanField(default=True)
    total_jobs = models.IntegerField(default=0)
    location = models.PointField(null=True, blank=True)
    completed_jobs = models.IntegerField(default=0)
    cancelled_jobs = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user} - {self.skills}'


class Client(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='client')
    location = models.PointField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user}'
