from django.urls import path
from . import views

urlpatterns = [
    path('message/<int:sender_id>/<int:receiver_id>',
         views.MessageAPIView.as_view(), name='message'),
    path('user-messages/<int:user_id>',
         views.UserMessagesAPIView.as_view(), name='user-messages'),
]
