from django.contrib.auth.models import User
from django.db import models

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.TextField()
    experience = models.TextField()

    def __str__(self):
        return f"Resume for {self.user.username}"
