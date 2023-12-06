from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as DistanceFunc

from ..models import Job
from ..serializers import JobSerializer
from django.contrib.gis.geos import Point
from users.models import Worker
from notifications.models import Notifications
from django.shortcuts import get_object_or_404
from utils.helper import send_sms

MAX_DISTANCE = 30  # in km


class JobList(generics.ListCreateAPIView):
    queryset = Job.objects.filter(status='open').all()
    serializer_class = JobSerializer
    filterset_fields = ['category__title', 'job_type',
                        'title', 'budget', 'labors_required', 'status']
    search_fields = ['title', 'job_type', 'category__title',
                     'budget', 'labors_required', 'status']

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            # anyone can view the jobs
            permission_classes = [permissions.AllowAny]
        else:
            # only authenticated users can create jobs
            permission_classes = [permissions.IsAuthenticated]
        return [permissions() for permissions in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        worker = Worker.objects.filter(user=self.request.user).first()

        if worker:
            user_location = worker.location
            skills = worker.skills

            if skills is not None:
                query = Q()
                for skill in skills:
                    query |= Q(category__title__icontains=skill)
                queryset = queryset.filter(query)

            # filter queryset that matches job city with worker city
            city_matched_queryset = queryset.filter(
                Q(city__icontains=worker.user.city))
            # Filter jobs within a distance of 30km from the user's location
            queryset = city_matched_queryset.annotate(distance=DistanceFunc(
                'location', user_location)).filter(distance__lte=Distance(km=MAX_DISTANCE))

            if queryset.count() == 0:
                return city_matched_queryset
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = JobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # save location from longitude and latitude

        try:
            longitude = request.data.get('longitude', 0)
            latitude = request.data.get('latitude', 0)
            longitude = float(longitude)
            latitude = float(latitude)
            location = Point(longitude, latitude)
        except:
            location = Point(None, None)
        finally:
            serializer.save(user=self.request.user, location=location)

        # send notifications to workers within 30km
        workers = Worker.objects.filter(
            location__distance_lte=(location, Distance(km=30)))
        msg_control = 1
        for worker in workers:
            notification = Notifications.objects.create(
                reciever_id=worker.user.id,
                title='New Job Posted',
                body=f'A new job has been posted in {request.data.get("address")}.',
            )
            # send notification to worker's mobile number
            if msg_control:
                msg_control = 0  # send only one message because of trial account
                send_sms(request=None, body=notification.body,
                         to='+923195789002')

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            # anyone can view the jobs with id
            permission_classes = [permissions.AllowAny]
        else:
            # only authenticated users can update/delete jobs
            permission_classes = [permissions.IsAuthenticated]
        return [permissions() for permissions in permission_classes]

    def update(self, request, *args, **kwargs):
        job = self.get_object()
        if job.user != self.request.user:  # only the user who posted the job can update it
            return Response({'response': "You don't have permission to update this job."})
        if request.data.get('attachment'):
            # if job attachment is a link don't update in the patch request.
            # Only update if it's a file
            attachment = request.data['attachment']
            if isinstance(attachment, InMemoryUploadedFile):
                job.attachment = attachment
            else:
                # make copy of attachment and remove it from request.data
                copy_of_attachment = request.data['attachment'].copy()
                copy_of_attachment.pop('attachment')

        serializer = JobSerializer(job, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        # set mutations true to remove immutable error

        job = get_object_or_404(Job, pk=kwargs['pk'])
        if job.user != self.request.user:
            return Response({'response': "You don't have permission to update this job."})
        if request.data.get('worker_id'):
            worker = Worker.objects.get(pk=request.data.get('worker_id'))
            job.worker = worker

        job.save()
        serializer = JobSerializer(job, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        job = self.get_object()
        if job.user != self.request.user:  # only the user who posted the job can delete it
            return Response({'response': "You don't have permission to delete this job."})
        job.delete()
        return Response({'response': "Job deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class ListUserCreatedJobs(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    filterset_fields = ['category__title', 'job_type', ]
    search_fields = ['title', 'job_type', 'category__title', ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # get all jobs created by the user
        return Job.objects.filter(user=self.request.user).all()


class UserCreatedJobDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    filterset_fields = ['category__title', 'job_type', ]
    search_fields = ['title', 'job_type', 'category__title', ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user).all()


class WorkerCompletedJobs(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        worker = Worker.objects.filter(user=self.request.user).first()
        return Job.objects.filter(worker=worker, status='completed').all()

class WorkerContractedJobs(generics.ListAPIView): 
    # to which worker is assigned 
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        worker = Worker.objects.filter(user=self.request.user).first()
        return Job.objects.filter(worker=worker).all()
    
    