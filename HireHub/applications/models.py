from django.db import models
from jobs.models import Job_Create

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Reviewed', 'Reviewed'),
    ('Interview', 'Interview'),
    ('Offer', 'Offer'),
    ('Rejected', 'Rejected'),
]


class JobApplication(models.Model):
    job = models.ForeignKey(
        Job_Create,
        on_delete=models.CASCADE,
        related_name='applications',
        null=True,
        blank=True,
    )
    applicant_name = models.CharField(max_length=100)
    applicant_email = models.EmailField()
    job_title = models.CharField(max_length=200, blank=True)  # store job title as text
    job_company = models.CharField(max_length=200, blank=True)  # optional company name
    job_location = models.CharField(max_length=200, blank=True)  # optional location

    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    applied_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        job_title = self.job.title if self.job else self.job_title
        return f"{self.applicant_name} - {job_title or 'Unassigned'}"