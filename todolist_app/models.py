from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TaskList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    task = models.CharField(max_length=300)
    done = models.BooleanField(default=False)
    
    def __str__(self):
        return self.task + " - " + str(self.done)
    
    
class ContactFormLog(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    action_time = models.DateTimeField(null=True, blank=True)
    is_success = models.BooleanField(default=False)
    is_error = models.BooleanField(default=False)
    error_message = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.email + " | " + self.subject