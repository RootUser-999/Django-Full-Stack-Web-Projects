from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobApplicationForm
from .models import JobApplication
from jobs.models import Job_Create

# Apply for a job
def apply_job(request, job_id):
    if not request.user.is_authenticated:
        return redirect('login')

    job = get_object_or_404(Job_Create, id=job_id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.job_title = job.title
            application.job_company = job.company
            application.job_location = job.location
            application.applicant_name = request.user.get_full_name() or request.user.username
            application.applicant_email = request.user.email
            application.save()
            return render(request, 'applications/application_success.html', {'application': application})
    else:
        initial_data = {
            'applicant_name': request.user.get_full_name() or request.user.username,
            'applicant_email': request.user.email,
        }
        form = JobApplicationForm(initial=initial_data)

    return render(request, 'applications/apply_job.html', {'form': form, 'job': job})


# Dashboard showing all applications for current user
def application_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    applicant_email = request.user.email or request.user.username
    applications = JobApplication.objects.filter(applicant_email=applicant_email).select_related('job')
    
    return render(request, 'accounts/profile.html', {'applications': applications})