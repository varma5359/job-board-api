"""
Models for the accounts app.
Defines a custom User model with a 'role' field so we can
distinguish between recruiters and applicants.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model that extends Django's default AbstractUser.

    Adds a 'role' field to identify whether the user is a
    recruiter (who posts jobs) or an applicant (who applies).

    Attributes:
        role (str): Either 'recruiter' or 'applicant'.
    """

    ROLE_CHOICES = (
        ('recruiter', 'Recruiter'),
        ('applicant', 'Applicant'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='applicant',
        help_text="Role of the user: recruiter or applicant."
    )

    def is_recruiter(self):
        """
        Check if the user is a recruiter.

        Returns:
            bool: True if role is 'recruiter', else False.
        """
        return self.role == 'recruiter'

    def is_applicant(self):
        """
        Check if the user is an applicant.

        Returns:
            bool: True if role is 'applicant', else False.
        """
        return self.role == 'applicant'

    def __str__(self):
        """Return username with role for admin display."""
        return f"{self.username} ({self.role})"