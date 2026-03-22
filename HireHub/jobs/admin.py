from .models import Job_Create
from django.contrib import admin

@admin.register(Job_Create)
class JobCreateAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'salary', 'posted_date')
    
