"""
URL routes for the jobs app.
"""

from django.urls import path
from .views import (
    list_jobs, create_job, job_detail, update_job, delete_job,
    apply_to_job, my_applications, view_applications, update_application_status,
)

urlpatterns = [
    # Job endpoints
    path('jobs/', list_jobs, name='list_jobs'),
    path('jobs/create/', create_job, name='create_job'),
    path('jobs/<int:job_id>/', job_detail, name='job_detail'),
    path('jobs/<int:job_id>/update/', update_job, name='update_job'),
    path('jobs/<int:job_id>/delete/', delete_job, name='delete_job'),

    # Application endpoints
    path('jobs/<int:job_id>/apply/', apply_to_job, name='apply_to_job'),
    path('jobs/<int:job_id>/applications/', view_applications, name='view_applications'),
    path('my-applications/', my_applications, name='my_applications'),
    path('applications/<int:app_id>/status/', update_application_status, name='update_status'),
]