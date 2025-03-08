from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import JobCreateView, JobListView, JobRetrieveUpdateDestoryView, JobApplicationCreateView, JobApplicationListView, JobApplicationRetrieveUpdateDestoryView, UpdateApplicationStatusView,UserRegistrationView, UserLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/create/', JobCreateView.as_view(), name='job-create'),
    path('jobs/<int:pk>/', JobRetrieveUpdateDestoryView.as_view(), name='job-detail'),
    path('jobs/<int:pk>/applications/', JobApplicationListView.as_view(), name='job-application-list'),
    path('jobs/<int:pk>/applications/create/', JobApplicationCreateView.as_view(), name='job-application-create'),
    path('jobs/<int:job_pk>/applications/<int:pk>/', JobApplicationRetrieveUpdateDestoryView.as_view(), name='job-application-create'),
    path('jobs/<int:job_id>/applications/<int:application_id>/update/', UpdateApplicationStatusView.as_view(), name='update-application-status')   
]