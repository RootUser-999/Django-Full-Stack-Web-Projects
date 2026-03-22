from django.contrib import messages
from django.shortcuts import render
from .forms import JobCreateForm
from django.http import HttpResponseRedirect
# Create your views here.

def create_job(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=JobCreateForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Job created successfully!')
                return HttpResponseRedirect('/jobs/create/')
        else:
            form=JobCreateForm()
        return render(request,'jobs/job_create.html',{'form':form})
    else:
        messages.error(request, 'You must be logged in to create a job.')
        return HttpResponseRedirect('/accounts/login/')
    
from .models import Job_Create

def job_view(request):
    
        jobs = Job_Create.objects.all()   # ✅ correct
        return render(request, 'jobs/job_list.html', {'jobs': jobs})
   
def job_details(request,id ):
    job_id = id  # Get the job ID from the URL parameter
    if job_id:
        try:
            job = Job_Create.objects.get(id=job_id)  # Fetch the job details using the ID
            return render(request, 'jobs/job_details.html', {'job': job})
        except Job_Create.DoesNotExist:
            messages.error(request, 'Job not found.')
            return HttpResponseRedirect('/jobs/')
    else:
        messages.error(request, 'No job ID provided.')
        return HttpResponseRedirect('/jobs/')        

def job_success(request):
    return render(request, 'jobs/job_success.html')