from django.core.mail import send_mail
from django.conf import settings

def send_application_status_email(applicant_email, job_title, status):
    subject = f"Your Application for {job_title} - {status.capitalize()}"
    message = f"""
        Hello,Your application for the position of {job_title} has been {status}.
        
        Thank you for applying!

        Best regards,
        Job Board Team
    """

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [applicant_email])