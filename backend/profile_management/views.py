# views.py in the profile_management app

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import WorkerSkill
from .serializers import WorkerSkillSerializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def worker_skill(request):
     # Check if the user is in the 'worker' group
    if not request.user.groups.filter(name='worker').exists():
        return Response({"message": "You are not a Worker"}, status=status.HTTP_403_FORBIDDEN)
    
    # Handle GET request to retrieve worker skills   
    if request.method == 'GET':
            workerskill = WorkerSkill.objects.select_related('user').filter(user=request.user)
            serialized_workerskill = WorkerSkillSerializer(workerskill, many=True)
            return Response(serialized_workerskill.data)
            
    # Handle POST request logic to add a new worker skill
    elif request.method == 'POST':
            serializer = WorkerSkillSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # Handle PUT request logic to update a worker skill      
    elif request.method == 'PUT':
            try:
                skill_to_update = WorkerSkill.objects.get(user=request.user, id=request.data['skill_id'])
            except WorkerSkill.DoesNotExist:
                return Response({"message": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = WorkerSkillSerializer(skill_to_update, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
   # Handle DELETE request logic to delete a worker skill
    elif request.method == 'DELETE':
        try:
            skill_to_delete = WorkerSkill.objects.get(user=request.user, id=request.data['skill_id'])
        except WorkerSkill.DoesNotExist:
            return Response({"message": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)

        skill_to_delete.delete()
        return Response({"message": "Skill deleted"}, status=status.HTTP_204_NO_CONTENT)
                
