"""
Models for the jobs app.
Defines the Job model which recruiters create.
"""

from django.db import models
from django.conf import settings


class Job(models.Model):
    """
    Represents a job posting created by a recruiter.

    Attributes:
        recruiter (User): The recruiter who posted this job.
        title (str): Job title (e.g. 'Backend Developer').
        company (str): Company name.
        location (str): Job location.
        description (str): Full job description.
        salary (str): Optional salary info.
        created_at (datetime): Auto-set when job is created.
    """

    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs',
        help_text="The recruiter who posted this job."
    )
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """Return a readable label for admin display."""
        return f"{self.title} at {self.company}"

class Application(models.Model):
    """
    Represents an applicant's application to a job.

    Stores the applicant's submitted details: name, contact,
    experience, skills, cover letter, and resume.

    A user can apply to a job only once (enforced by unique_together).
    Recruiters can update the status to shortlist or reject.

    Attributes:
        job (Job): The job being applied to.
        applicant (User): The applicant who applied.
        full_name (str): Applicant's full name.
        email (str): Contact email.
        phone (str): Contact phone number.
        location (str): Current city/location.
        experience_years (int): Years of experience.
        skills (str): Comma-separated skills.
        cover_letter (str): Applicant's message.
        resume (File): Uploaded resume (PDF/DOC).
        status (str): pending / shortlisted / rejected.
        applied_at (datetime): Auto-set when applied.
    """

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='applications'
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='applications'
    )

    # ---- Applicant details captured at apply time ----
    full_name = models.CharField(max_length=150)
    email = models.EmailField(default='unknown@example.com')
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField(default=0)
    skills = models.CharField(
        max_length=300,
        help_text="Comma-separated skills (e.g. Python, Django, SQL)"
    )

    cover_letter = models.TextField()
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True,
        help_text="Upload PDF or DOC (max 5MB)."
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']

    def __str__(self):
        """Return readable label for admin."""
        return f"{self.full_name} → {self.job.title}"