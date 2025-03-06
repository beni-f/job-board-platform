from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, UserRegistrationView, UserLoginView, JobApplicationViewset

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'applications', JobApplicationViewset, basename='application')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
]