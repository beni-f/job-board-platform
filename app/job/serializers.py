from rest_framework import serializers
from .models import Job, CustomUser, Category, JobApplication
from django.utils.timezone import now

class JobSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    custom_category = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Job
        fields = ['title', 'recruiter', 'description', 'location', 'category', 'salary',  'custom_category', 'date_posted', 'job_deadline']
        extra_kwargs = {
            'recruiter': {'read_only': True},
            'date_posted': {'read_only': True}
        }
    
    def validate(self, data):
        custom_category = data.get('custom_category')
        if custom_category:
            category, created = Category.objects.get_or_create(name=custom_category)
            data['category'] = category

        if not data.get('category') and not data.get('custom_category'):
            raise serializers.ValidationError('Category is required')
        return data
    
    def validate_job_deadline(self, value):
        if value <= now():
            return serializers.ValidationError('Deadline must be in the future')
        return value

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name',
         'username', 'email', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
        
class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['job', 'applicant', 'application_date', 'status', 'cover_letter', 'resume']
        extra_kwargs = {
            'applicant': {'read_only': True},
            'status': {'read_only': True},
            'application_date': {'read_only': True}
        }

class JobApplicationStatusSerializer(serializers.ModelSerializer):
    STATUS_CHOICES =(
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    class Meta:
        model = JobApplication
        fields = ['status']
    