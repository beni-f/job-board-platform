# Job Board Backend

A full-featured job board platform built with Django REST Framework (DRF) and React, allowing users to post jobs, applying for positions, and manage applications.

## Features
- User Authentication with JWT
- Job posting and application system
- Email notifications for application status updates
- Admin panel for managing jobs and users

## Installation
### Prerequisites
- Python 3.10+
- PostgreSQL or SQLite
- Redis (for caching and task queue)

## Backend Setup
1. **Clone the repository:**
    ```sh
    git clone https://github.com/beni-f/job-board-platform.git
    cd job-board-platform
    ```
2. **Create a virtual environment and activate it**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
4. **Set up environment variables:** Create a .env file in the ./app directory and add
    ```sh
    DB_NAME= 'your_db_name'
    DB_USER = 'your_db_user'
    DB_PASSWORD = 'your_db_password'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'your_email@example.com'
    EMAIL_HOST_PASSWORD = 'your_email_password'
    DEFAULT_FROM_EMAIL = 'your_email@example.com'
    ```
5. **Apply migrations and create a superuser**
    ```sh
    python3 manage.py migrate
    python3 manage.py createsuperuser
    ```
6. **Run the server**:
    ```sh
    python3 manage.py runserver
    ```

## API Endpoints
### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - Logout

### Jobs
- `GET /api/jobs/` - List all jobs
- `POST /api/jobs/create` - Create a new job (Recruiter only)
- `GET /api/jobs/{id}/` - Retrieve a job
- `PUT /api/jobs/{id}/` - Update a job (Recruiter of the job only)
- `DELETE /api/jobs/{id}/` - Delete a job (Recruiter of the job only)

### Applications
- `GET /api/jobs/{job_id}/applications` - List applications for a specific job (Recruiter of the job only)
- `POST /api/jobs/{job_id}/applications/apply` - Apply for a job (Job seeker only)
- `GET /api/jobs/{job_id}/applications/{application_id}` - Retrieve the job application (Recruiter of the job and the applier only)
- `PUT /api/jobs/{job_id}/applications/{application_id}/update-status` - Update application status (Recruiter of the job only)
- `PUT /api/jobs/{job_id}/applications/{application_id}` - Update application (Job applier only)

## License
This project is licensed under the MIT license.