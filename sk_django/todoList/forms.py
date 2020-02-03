from django.forms import ModelForm
from .models import Task
from .models import Comment

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields =[ 'taskname', 'description' , 'category']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'views_count']
