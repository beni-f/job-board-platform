from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate

from .models import Job, CustomUser, JobApplication
from .serializers import JobSerializer, CustomUserSerializer, JobApplicationSerializer, JobApplicationStatusSerializer
from .permissions import IsEmployer, IsNotAuthenticated, IsApplicant, IsApplicantOrEmployer

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
    
class JobListView(ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'location']
    search_fields = ['title', 'location', 'category__name']
    ordering_fields = ['date_posted']


class JobCreateView(CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsEmployer]

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

class JobRetrieveUpdateDestoryView(RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method in ["PUT", "PATCH", "DELETE"]:
            return  [IsEmployer()]
        return [IsAuthenticated()]

class JobApplicationCreateView(CreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsApplicant]

    def perform_create(self, serializer):
        job_id = self.kwargs.get('pk')
        job = get_object_or_404(Job, pk=job_id)
        serializer.save(applicant=self.request.user, job=job)

class JobApplicationListView(ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsEmployer]

    def get_queryset(self):
        job_id = self.kwargs.get('pk')
        return JobApplication.objects.filter(job_id=job_id)

class JobApplicationRetrieveUpdateDestoryView(RetrieveUpdateDestroyAPIView):
    serializer_class = JobApplicationSerializer
    
    def get_queryset(self):
        job_id = self.kwargs.get('job_pk')
        return JobApplication.objects.filter(job_id=job_id)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsApplicantOrEmployer()]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsApplicant()]
        return [IsAuthenticated()]


class UserRegistrationView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsNotAuthenticated]

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        return Response({"error": F"Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateApplicationStatusView(UpdateAPIView):
    serializer_class = JobApplicationStatusSerializer
    permission_classes = [IsEmployer]

    def get_object(self):
        job_id = self.kwargs.get('job_id')
        application_id = self.kwargs.get('application_id')

        return get_object_or_404(JobApplication, id=application_id, job__id=job_id)

    def perform_update(self, serializer):
        user = self.request.user
        if user.role != 'employer':
            raise serializers.ValidationError("Only employers can update the status.")
        
        serializer.save()
