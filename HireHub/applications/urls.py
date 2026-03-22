from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply'),
    path('dashboard/', views.application_dashboard, name='dashboard'),
]