from django.contrib import admin
from .models import JobApplication  # updated model name

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant_name', 'applicant_email', 'job_title', 'applied_date', 'status')
    search_fields = ('applicant_name', 'applicant_email', 'job_title', 'job_company')
    list_filter = ('status', 'applied_date')