"""
Views for the jobs app.
Handles job listing, creation, update and delete.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Job
from .serializers import JobSerializer
from utils.responses import success_response, error_response


@api_view(['GET'])
@permission_classes([AllowAny])
def list_jobs(request):
    """
    Return a list of all jobs.

    Method: GET
    URL: /api/jobs/
    Auth: Not required.

    Returns:
        200: List of jobs.
    """
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return success_response(
        data=serializer.data,
        message=f"{jobs.count()} jobs found.",
        status=200
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_job(request):
    """
    Allow a recruiter to create a new job posting.

    Method: POST
    URL: /api/jobs/
    Auth: Required (recruiter only).
    Body: { title, company, location, description, salary }

    Returns:
        201: Job created.
        403: If user is not a recruiter.
        400: Validation errors.
    """
    if not request.user.is_recruiter():
        return error_response(
            message="Only recruiters can post jobs.",
            status=403
        )

    serializer = JobSerializer(data=request.data)

    if not serializer.is_valid():
        return error_response(
            message="Invalid job data.",
            status=400,
            errors=serializer.errors
        )

    serializer.save(recruiter=request.user)
    return success_response(
        data=serializer.data,
        message="Job created successfully.",
        status=201
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def job_detail(request, job_id):
    """
    Return details of a single job.

    Method: GET
    URL: /api/jobs/<id>/
    Auth: Not required.

    Returns:
        200: Job details.
        404: Job not found.
    """
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return error_response(message="Job not found.", status=404)

    serializer = JobSerializer(job)
    return success_response(data=serializer.data, status=200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_job(request, job_id):
    """
    Allow the owner recruiter to update a job.

    Method: PUT
    URL: /api/jobs/<id>/
    Auth: Required (job owner only).

    Returns:
        200: Job updated.
        403: Not the owner.
        404: Job not found.
    """
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return error_response(message="Job not found.", status=404)

    if job.recruiter != request.user:
        return error_response(
            message="You can only edit your own jobs.",
            status=403
        )

    serializer = JobSerializer(job, data=request.data, partial=True)

    if not serializer.is_valid():
        return error_response(
            message="Invalid job data.",
            status=400,
            errors=serializer.errors
        )

    serializer.save()
    return success_response(
        data=serializer.data,
        message="Job updated successfully.",
        status=200
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_job(request, job_id):
    """
    Allow the owner recruiter to delete a job.

    Method: DELETE
    URL: /api/jobs/<id>/
    Auth: Required (job owner only).

    Returns:
        200: Job deleted.
        403: Not the owner.
        404: Job not found.
    """
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return error_response(message="Job not found.", status=404)

    if job.recruiter != request.user:
        return error_response(
            message="You can only delete your own jobs.",
            status=403
        )

    job.delete()
    return success_response(message="Job deleted successfully.", status=200)


from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_to_job(request, job_id):
    """
    Allow an applicant to apply to a specific job.

    Method: POST
    URL: /api/jobs/<id>/apply/
    Auth: Required (applicant only).
    Body: { cover_letter }

    Returns:
        201: Application created.
        403: If user is not an applicant.
        404: Job not found.
        400: Duplicate application or validation errors.
    """
    if not request.user.is_applicant():
        return error_response(
            message="Only applicants can apply to jobs.",
            status=403
        )

    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return error_response(message="Job not found.", status=404)

    if Application.objects.filter(job=job, applicant=request.user).exists():
        return error_response(
            message="You already applied to this job.",
            status=400
        )

    serializer = ApplicationSerializer(data=request.data)

    if not serializer.is_valid():
        return error_response(
            message="Invalid application data.",
            status=400,
            errors=serializer.errors
        )

    serializer.save(job=job, applicant=request.user)
    return success_response(
        data=serializer.data,
        message="Application submitted successfully.",
        status=201
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_applications(request):
    """
    Return all applications submitted by the logged-in applicant.

    Method: GET
    URL: /api/my-applications/
    Auth: Required (applicant only).

    Returns:
        200: List of applications.
        403: If user is not an applicant.
    """
    if not request.user.is_applicant():
        return error_response(
            message="Only applicants can view their applications.",
            status=403
        )

    apps = Application.objects.filter(applicant=request.user)
    serializer = ApplicationSerializer(apps, many=True)
    return success_response(
        data=serializer.data,
        message=f"{apps.count()} applications found.",
        status=200
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_applications(request, job_id):
    """
    Return all applications for a job (recruiter owner only).

    Method: GET
    URL: /api/jobs/<id>/applications/
    Auth: Required (job owner recruiter).

    Returns:
        200: List of applications.
        403: If not the job owner.
        404: Job not found.
    """
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return error_response(message="Job not found.", status=404)

    if job.recruiter != request.user:
        return error_response(
            message="You can only view applications for your own jobs.",
            status=403
        )

    apps = Application.objects.filter(job=job)
    serializer = ApplicationSerializer(apps, many=True)
    return success_response(
        data=serializer.data,
        message=f"{apps.count()} applications found.",
        status=200
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_application_status(request, app_id):
    """
    Allow recruiter to update an application's status.

    Method: PUT
    URL: /api/applications/<id>/status/
    Auth: Required (job owner recruiter).
    Body: { status: 'shortlisted' | 'rejected' | 'pending' }

    Returns:
        200: Status updated.
        400: Invalid status.
        403: If not the job owner.
        404: Application not found.
    """
    try:
        application = Application.objects.get(id=app_id)
    except Application.DoesNotExist:
        return error_response(message="Application not found.", status=404)

    if application.job.recruiter != request.user:
        return error_response(
            message="You can only manage applications for your own jobs.",
            status=403
        )

    new_status = request.data.get('status')
    if new_status not in ['pending', 'shortlisted', 'rejected']:
        return error_response(
            message="Status must be pending, shortlisted, or rejected.",
            status=400
        )

    application.status = new_status
    application.save()

    serializer = ApplicationSerializer(application)
    return success_response(
        data=serializer.data,
        message=f"Application marked as {new_status}.",
        status=200
    )


from django.shortcuts import render


def page_login(request):
    """Render login page."""
    return render(request, 'login.html')


def page_register(request):
    """Render register page."""
    return render(request, 'register.html')


def page_jobs(request):
    """Render jobs listing page."""
    return render(request, 'jobs.html')


def page_recruiter(request):
    """Render recruiter dashboard (post job + manage applications)."""
    return render(request, 'recruiter.html')


def page_my_applications(request):
    """Render applicant's own applications page."""
    return render(request, 'my_applications.html')