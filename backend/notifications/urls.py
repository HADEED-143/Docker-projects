from .views import NotificationsList, NotificationsDetail
from django.urls import path

urlpatterns = [
    path('job/notifications/', NotificationsList.as_view()),
    path('job/notifications/<int:pk>/', NotificationsDetail.as_view()),
]