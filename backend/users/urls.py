from django.urls import path
from . import views
urlpatterns = [
    path("user-info/", views.user_info),
    path("user-info/<int:user_id>", views.user_info_single),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('user/workers', views.search_workers, name='search-workers'),
    path('user/workers/<int:id>', views.view_or_update_worker_information, name='view-or-update-worker'),
    path("ping/", views.ping, name="ping")
]
