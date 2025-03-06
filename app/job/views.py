from django.shortcuts import render
from django.contrib.auth import authenticate

from .models import Job, CustomUser, JobApplication
from .serializers import JobSerializer, CustomUserSerializer, JobApplicationSerializer
from .permissions import IsEmployerOrAdmin, IsEmployer, IsNotAuthenticated, IsApplicant, IsApplicantOrEmployer, IsEmployerOfJob

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class JobViewSet(ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = []

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['create']:
            permission_classes = [IsEmployerOrAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsEmployer]
        else:
            permission_classes = [IsAuthenticated]
        return [permisson() for permisson in permission_classes]

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        job = self.get_object()
        serializer = self.get_serializer(job)
        return Response(serializer.data)

class JobApplicationViewset(ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsApplicant]
        elif self.action in ['list']:
            permission_classes = [IsEmployerOfJob]
        elif self.action in ['retrieve']:
            permission_classes = [IsApplicantOrEmployer]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsApplicant]
        else: 
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        application = self.get_object()
        serializer = self.get_serializer(application)
        return Response(serializer.data)

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
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)