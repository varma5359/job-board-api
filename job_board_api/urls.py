"""
Main URL configuration for the Job Board API project.
"""

from django.contrib import admin
from django.urls import path, include
from jobs.views import page_login, page_register, page_jobs,page_recruiter, page_my_applications


urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts (register, login)
    path('api/', include('accounts.urls')),

    # Jobs (list, create, detail, update, delete)
    path('api/', include('jobs.urls')),


    # Frontend pages
    path('', page_login, name='home'),
    path('login/', page_login, name='page_login'),
    path('register/', page_register, name='page_register'),
    path('jobs/', page_jobs, name='page_jobs'),
    path('recruiter/', page_recruiter, name='page_recruiter'),
    path('my-applications/', page_my_applications, name='page_my_applications'),
]