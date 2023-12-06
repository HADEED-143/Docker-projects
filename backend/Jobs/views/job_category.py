from rest_framework import generics, permissions
from ..models import JobCategory
from ..serializers import JobCategorySerializer

# Create your views here.
class JobCategoryList(generics.ListCreateAPIView):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    search_fields = ['title']
    ordering_fields = ['id']
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]  # anyone can view the job categories
        else: 
            permission_classes = [permissions.IsAdminUser]  # only admin can create job categories
        return [permissions() for permissions in permission_classes]
    
class JobCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    
    def get_permissions(self): 
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]  # anyone can view the job categories with id 
        else: 
            permission_classes = [permissions.IsAdminUser]  # only admin can update/delete job categories
        return [permissions() for permissions in permission_classes]
    
