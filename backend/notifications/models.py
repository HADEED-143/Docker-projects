from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class Notifications(models.Model):
    reciever = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=100)
    viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
