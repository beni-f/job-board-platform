from rest_framework.permissions import BasePermission

class IsEmployerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'employer' or request.user.is_staff
    
class IsEmployer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.recruiter
    
class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated
    
class IsApplicant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'job_seeker'
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == 'job_seeker'
    
class IsApplicantOrEmployer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return request.user == obj.applicant or request.user == obj.job.recruiter
    
class IsEmployerOfJob(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'employer'
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.job.recruiter