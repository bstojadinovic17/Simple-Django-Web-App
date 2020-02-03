from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taskname = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=50)
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.taskname

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default="", editable=False)
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    views_count = models.IntegerField(default=0)


    def __str__(self):
        return self.content