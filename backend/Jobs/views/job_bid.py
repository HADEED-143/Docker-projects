from rest_framework import generics
from ..permissions import IsWorker
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from ..permissions import IsWorker
from ..serializers import JobBidSerializer
from ..models import JobBid
from users.models import Worker
from notifications.models import Notifications
from ..models import Job


class JobBidView(generics.ListCreateAPIView):
    queryset = JobBid.objects.all()
    serializer_class = JobBidSerializer
    filterset_fields = ['job__title', 'offer', ]
    search_fields = ['job__title', 'offer', 'worker', ]

    def get_permission(self):
        permission_classes = []
        if self.request.method == 'POST':
            permission_classes = [IsWorker]  # only worker places the bid
        else:
            # only authenticated users with client role can view the bids
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            # return all bids for the jobs posted by the user
            return JobBid.objects.filter(job__user=user)
        return JobBid.objects.none()  # return empty queryset if user is not authenticated

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = JobBidSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if not user and user.role != 'worker':
            return Response({'response': "You don't have permission to place a bid."})
        worker_id = request.data['worker_id']
        if not worker_id:
            return Response({'response': "Worker id is required."})

        serializer = JobBidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        worker = Worker.objects.get(pk=worker_id)
        serializer.save(worker=worker)
        # send notification to the client who posted the job
        job = Job.objects.get(pk=request.data['job_id'])
        Notifications.objects.create(
            reciever=job.user, title='A new request received', body=f'{worker.user.first_name} {worker.user.last_name} has placed a bid on your job {job.title}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobBidDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobBid.objects.all()
    serializer_class = JobBidSerializer
    filterset_fields = ['job', 'worker', 'job__status']
    search_fields = ['job', 'worker', 'job__status']

    # def get_queryset(self):
    #     user = self.request.user
    #     if user and user.role == 'worker' and JobBid.objects.get(pk=user.id):
    #         return JobBid.objects.all()
    #     return JobBid.objects.none()

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsWorker]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if not user and not user == self.get_object().worker and user.role != 'worker':
            return Response({'response': "You don't have permission to update this bid."})
        serializer = JobBidSerializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if not user and not user == self.get_object().worker:
            return Response({'response': "You don't have permission to delete this bid."})
        self.get_object().delete()
        return Response({'response': "Bid deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class SpecificJobBids(generics.ListAPIView):
    serializer_class = JobBidSerializer
    filterset_fields = ['job', 'worker',]
    search_fields = ['job', 'worker',]

    def get_queryset(self):
        job_id = self.kwargs['job_pk']
        if job_id:
            return JobBid.objects.filter(job__id=job_id).all()
        return Response({'response': "Job not found."}, status=status.HTTP_404_NOT_FOUND)

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = JobBidSerializer(queryset, many=True)
        return Response(serializer.data)


class SpecificJobBidDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobBidSerializer
    filterset_fields = ['job', 'worker',]
    search_fields = ['job', 'worker',]

    def get_queryset(self):
        job_id = self.kwargs['job_pk']
        bid_id = self.kwargs['pk']
        if job_id and bid_id:
            return JobBid.objects.filter(job__id=job_id, id=bid_id).all()
        return Response({'response': "Job bid not found."}, status=status.HTTP_404_NOT_FOUND)

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = JobBidSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if not user and not user == self.get_object().worker:
            return Response({'response': "You don't have permission to update this bid."})
        serializer = JobBidSerializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if not user and not user == self.get_object().worker:
            return Response({'response': "You don't have permission to delete this bid."})
        self.get_object().delete()
        return Response({'response': "Bid deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class UserBidList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsWorker]
    serializer_class = JobBidSerializer
    filterset_fields = ['job__title', 'worker__user__first_name',
                        'worker__user__last_name', 'job__budget', 'offer']
    search_fields = ['job__title', 'worker__user__first_name',
                     'worker__user__last_name', 'job__budget', 'offer']

    def get_queryset(self):
        user = self.request.user
        worker = Worker.objects.filter(user=user).first()

        if worker:
            return JobBid.objects.filter(worker=worker).all()
        return JobBid.objects.none()


class UserBidDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsWorker]
    serializer_class = JobBidSerializer
    filterset_fields = ['job__title', 'worker__user__first_name',
                        'worker__user__last_name', 'job__budget', 'offer']
    search_fields = ['job__title', 'worker__user__first_name',
                     'worker__user__last_name', 'job__budget', 'offer']

    def get_queryset(self):
        user = self.request.user
        worker = Worker.objects.filter(user=user).first()

        if worker:
            return JobBid.objects.filter(worker=worker).all()
        return JobBid.objects.none()
