from django.contrib.auth.models import User
from django.db import models

# Create your models here.
 
class Job(models.Model):  
    title = models.CharField(max_length=100)  
    company = models.CharField(max_length=100)
    required_skills = models.TextField()

    def __str__(self):  
        return self.title