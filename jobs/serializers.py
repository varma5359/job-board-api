"""
Serializers for the jobs app.
Converts Job model instances to/from JSON.
"""

from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for the Job model.

    Includes recruiter username (read-only) so clients
    know who posted each job.
    """

    recruiter_username = serializers.CharField(
        source='recruiter.username',
        read_only=True
    )

    class Meta:
        model = Job
        fields = (
            'id',
            'recruiter',
            'recruiter_username',
            'title',
            'company',
            'location',
            'description',
            'salary',
            'created_at',
        )
        read_only_fields = ('id', 'recruiter', 'created_at')


from .models import Job, Application

class ApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for job applications.

    Captures applicant details: name, contact, experience, skills,
    cover letter, and resume. Adds nested job info and resume URL.
    """

    applicant_username = serializers.CharField(
        source='applicant.username', read_only=True
    )
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_company = serializers.CharField(source='job.company', read_only=True)
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = (
            'id',
            'job',
            'job_title',
            'job_company',
            'applicant',
            'applicant_username',

            # Applicant details
            'full_name',
            'email',
            'phone',
            'location',
            'experience_years',
            'skills',
            'cover_letter',
            'resume',
            'resume_url',

            # Status
            'status',
            'applied_at',
        )
        read_only_fields = ('id', 'applicant', 'status', 'applied_at')
        extra_kwargs = {
            'job': {'required': False, 'write_only': True},
            'resume': {'required': False},
        }

    def get_resume_url(self, obj):
        """
        Return the absolute URL of the uploaded resume, if any.

        Args:
            obj (Application): The application instance.

        Returns:
            str | None: Full URL to the resume file, or None.
        """
        if not obj.resume:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.resume.url)
        return obj.resume.url

    def validate_experience_years(self, value):
        """
        Ensure experience is between 0 and 60 years.

        Args:
            value (int): Years of experience.

        Returns:
            int: Validated value.

        Raises:
            ValidationError: If out of range.
        """
        if value < 0 or value > 60:
            raise serializers.ValidationError(
                "Experience must be between 0 and 60 years."
            )
        return value

    def validate_phone(self, value):
        """
        Ensure phone number has at least 10 digits.

        Args:
            value (str): Phone number.

        Returns:
            str: Validated phone.

        Raises:
            ValidationError: If invalid.
        """
        digits = ''.join(filter(str.isdigit, value))
        if len(digits) < 10:
            raise serializers.ValidationError(
                "Phone must contain at least 10 digits."
            )
        return value