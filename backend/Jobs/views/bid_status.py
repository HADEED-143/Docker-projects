from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from utils.helper import BID_STATUS

from ..models import JobBid
from ..serializers import JobBidSerializer


class JobBidStatus(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobBidSerializer
    queryset = JobBid.objects.all()

    def update(self, request, *args, **kwargs):
        job_bid = get_object_or_404(
            JobBid, pk=self.kwargs['pk'])  # current job bid
        print(job_bid.job.user, self.request.user)

        if job_bid.job.user != self.request.user:
            return Response({'response': "Permission not granted."}, status.HTTP_401_UNAUTHORIZED)

        job_status = self.request.data.get('status')
        if any(job_status in status for status in BID_STATUS):
            job_bid.status = job_status
            job_bid.save()
            return Response({'response': "Job bid status updated successfully."}, status=status.HTTP_200_OK)
        return Response({'response': "Invalid job status."}, status=status.HTTP_400_BAD_REQUEST)
