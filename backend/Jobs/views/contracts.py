from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from ..models import Job


class StartContractView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, job_id, format=None):
        job = Job.objects.get(id=job_id)
        if job.user != self.request.user:
            return Response({'response': "You don't have permission to start this job."})
        job.start_contract()
        return Response({'response': "Job status updated to 'In Progress'."}, status=status.HTTP_200_OK)


class EndContractView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, job_id, format=None):
        job = Job.objects.get(id=job_id)
        if job.user != self.request.user:
            return Response({'response': "You don't have permission to end this job."})
        job.complete_contract()
        return Response({'response': "Job status updated to 'Completed'."}, status=status.HTTP_200_OK)

class PauseContract(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, job_id, format=None): 
        job = Job.objects.get(id=job_id)
        if job.user != self.request.user: 
            return Response({'response': "You don't have permission to pause this job."})
        job.pause_contract()
        return Response({'response': "Job status updated to 'Paused'."}, status=status.HTTP_200_OK)
    

class CancelContract(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, job_id, format=None):
        job = Job.objects.get(id=job_id)
        if job.user != self.request.user: 
            return Response({'response': "You don't have permission to cancel this job."})
        job.cancel_contract()
        return Response({'response': "Job status updated to 'Cancelled'."}, status=status.HTTP_200_OK)
    
    