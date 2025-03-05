from rest_framework.permissions import BasePermission

class IsEmployerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'employer' or request.user.is_staff
    
class IsJobPosterOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.recruiter or request.method in ['GET', 'HEAD', 'OPTIONS']    
    
class IsNotAuthenticated(BasePermission):
    def has_object_permission(self, request, view, obj):
        return not request.user.is_authenticated