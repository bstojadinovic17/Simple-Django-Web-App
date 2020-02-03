from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name ='index'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<int:id>/', views.task, name='task'),
    path('tasks/newTask', views.newTask, name = 'newTask'),
    path('tasks/edit/<int:id>/', views.editTask, name= 'editTask'),
    path('tasks/delete/<int:id>/', views.deleteTask, name='deleteTask'),
    path('/loggedOut', views.loggedOut, name='loggedOut'),
    path('tasks/newComment/<int:id>/', views.newComment, name='newComment'),
    path('tasks/<int:id>/comments', views.showComments, name='comments'),
    path('tasks/comments/edit/<int:id>', views.editComment, name= 'editComment'),
    path('/comments/delete/<int:id>', views.deleteComment, name='deleteComment'),
]