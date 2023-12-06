# custom permission 
from rest_framework import permissions

class IsWorker(permissions.BasePermission): 
    def has_permission(self, request, view): 
        if request.user.role == 'worker' and request.user.is_authenticated:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: 
            return True
        return obj.worker == request.user