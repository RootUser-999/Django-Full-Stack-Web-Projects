from django.urls import path   
from . import views

urlpatterns = [
    path('create/', views.create_job, name='create_job'),
    path('jobs/', views.job_view, name='jobs'),
    path('jobs/<int:id>/', views.job_details, name='details'),
    path('job-success/', views.job_success, name='job_success'),
    ]