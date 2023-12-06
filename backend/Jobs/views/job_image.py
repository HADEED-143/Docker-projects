from rest_framework import generics 
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import Job, JobImages
from ..serializers import JobImageSerializer


class JobImagesView(generics.ListCreateAPIView): 
    queryset = JobImages.objects.all()
    serializer_class = JobImageSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]  # anyone can view the job images
        else: 
            permission_classes = [permissions.IsAuthenticated]  # only authenticated users can create job images
        return [permissions() for permissions in permission_classes]
    
    def create(self, request, *args, **kwargs):
        serializer = JobImageSerializer(data=request.data)
        job_id = self.kwargs['pk']
        job = get_object_or_404(Job, id=job_id)
        if job.user != self.request.user:
            return Response({'response': "You don't have permission to add images to this job."})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        job.job_images.add(serializer.instance)
        job.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)        
        
    
class ImageDetailView(generics.RetrieveUpdateDestroyAPIView): 
    serializer_class = JobImageSerializer
   
    def get_queryset(self):
        job_id = self.kwargs['job_pk']
        if job_id:
            job = get_object_or_404(Job, id=job_id)
            return job.job_images.all()
        return Response({'response': "Job not found."}, status=status.HTTP_404_NOT_FOUND)
    
    permissions_classes = [permissions.IsAuthenticated]
    filter_fields = ['job', ]
    search_fields = ['job', ]
    
    def update(self, request, *args, **kwargs):
        image = get_object_or_404(JobImages, id=self.kwargs['pk'])
        job = Job.objects.get(pk=self.kwargs['job_pk'])
        if not job or job.user != self.request.user: 
            return Response({'response': "You don't have permission to update this job image."})
        
        serializer = JobImageSerializer(image, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
    def destroy(self, request, *args, **kwargs):
        image = get_object_or_404(JobImages, id=self.kwargs['pk'])
        job = Job.objects.get(pk=self.kwargs['job_pk'])
        if job.user != self.request.user:
            return Response({'response': "You don't have permission to delete this job image."})
        image.delete()
        return Response({'response': "Job image deleted successfully."}, status=status.HTTP_204_NO_CONTENT)