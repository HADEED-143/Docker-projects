from django.urls import path
from . import views  # views folder in the same directory
from .views import StartContractView, EndContractView, CancelContract, PauseContract, WorkerCompletedJobs, WorkerContractedJobs

urlpatterns = [
    path('job-categories', views.JobCategoryList.as_view(), name='job-categories'),
    path('job-categories/<int:pk>', views.JobCategoryDetail.as_view(),
         name='job-category-detail'),
    path('jobs', views.JobList.as_view(), name='jobs'),
    path('user/jobs', views.ListUserCreatedJobs.as_view(), name='user-jobs'),
    path('user/jobs/<int:pk>', views.UserCreatedJobDetail.as_view(), name='user-jobs'),
    path('jobs/<int:pk>', views.JobDetail.as_view(), name='job-detail'),
    path('jobs/<int:pk>/images', views.JobImagesView.as_view(), name='job-images'),
    path('jobs/<int:job_pk>/images/<int:pk>',
         views.ImageDetailView.as_view(), name='job-image-detail'),
    path('jobs/bids', views.JobBidView.as_view(), name='job-bid'),
    path('jobs/user/bids', views.UserBidList.as_view(), name='job-user-bid'),
    path('jobs/user/bids/<int:pk>', views.UserBidDetail.as_view(),
         name='job-user-bid-detail'),
    path('jobs/<int:job_pk>/bids',
         views.SpecificJobBids.as_view(), name='job-specific-bid'),
    path('jobs/<int:job_pk>/bids/<int:pk>',
         views.SpecificJobBidDetail.as_view(), name='job-specific-bid'),
    path('jobs/bids/<int:pk>', views.JobBidDetail.as_view(), name='job-bid-detail'),
    path('jobs/bids/<int:pk>/mark',
         views.JobBidStatus.as_view(), name='job-bid-mark'),
    path('jobs/feedbacks',
         views.FeedbackList.as_view(), name='job-feedback'),
    path('jobs/feedbacks/<int:pk>', views.FeedbackDetail.as_view(),
         name='job-feedback-detail'),

    path('jobs/<int:job_id>/start-contract/',
         StartContractView.as_view(), name='start_contract'),
    path('jobs/<int:job_id>/end-contract/',
         EndContractView.as_view(), name='end_contract'),
    path('jobs/<int:job_id>/pause-contract/',
         PauseContract.as_view(), name='pause_contract'),
    path('jobs/<int:job_id>/cancel-contract/',
         CancelContract.as_view(), name='cancel_contract'),
    path('jobs/worker-completed', WorkerCompletedJobs.as_view(),
         name='worker-completed-jobs'),
    path('jobs/worker/contracted', WorkerContractedJobs.as_view(),
         name='worker-contracted-jobs')

]
