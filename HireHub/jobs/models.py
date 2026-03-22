from django.db import models

# Create your models here.
class Job_Create(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    location=models.CharField(max_length=100)
    salary=models.DecimalField(max_digits=10, decimal_places=2)
    company=models.CharField(max_length=100)
    posted_date=models.DateTimeField(auto_now_add=True)