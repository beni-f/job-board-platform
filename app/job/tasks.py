from django.utils import timezone
import pytz
from celery import shared_task
from .models import Job

@shared_task(name="job.tasks.delete_expired_jobs")
def delete_expired_jobs():
    now_utc = timezone.now()
    print(f"Current UTC time: {now_utc}")
    print(f"Now time {now_utc.astimezone(pytz.utc)}")
    expired_jobs = Job.objects.filter(job_deadline__lte=now_utc.astimezone(pytz.utc))

    print(f"Expired jobs found: {expired_jobs.count()}")

    if expired_jobs.exists():
        count, _ = expired_jobs.delete()
        print(f"Deleted {count} expired jobs")
    else:
        print("No expired jobs found")
