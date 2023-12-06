from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class WorkerSkill(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # one-to-one relationship with User
    skill_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s {self.skill_name}"
    
    
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Many-to-one relationship with User
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.degree
    
    
class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Many-to-one relationship with User
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
