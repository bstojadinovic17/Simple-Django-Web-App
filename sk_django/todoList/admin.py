from django.contrib import admin
from .models import Task
from .models import Comment

admin.site.register(Task)
admin.site.register(Comment)