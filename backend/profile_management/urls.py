from django.urls import path
from . import views

urlpatterns = [
    path('worker-skills/', views.worker_skill, name='worker-skill'),
]