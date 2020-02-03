from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import Comment
from .forms import CommentForm
from django.db.models import Avg, Max, Min, Sum
from collections import Counter
from django.contrib.auth.models import User
def index(req):
    if not req.user.is_authenticated:
        return render(req, 'index.html')
    else:
        return redirect('tasks')

@login_required
def tasks(req):
    allTasks = Task.objects.all()
    allComments = Comment.objects.all()
    ''' 
    Statistical data: 
    '''
    avgCommentViewCount = Comment.objects.all().aggregate(Avg('views_count'))['views_count__avg']
    commentsCount = Comment.objects.all().count()
    tasksCount = Task.objects.all().count()
    avgCommentPerTask = commentsCount/tasksCount
    maxViewedComment = Comment.objects.all().aggregate(Max('views_count')) ['views_count__max']
    commentWithMostViews = Comment.objects.get(views_count=maxViewedComment)

    minViewedComment = Comment.objects.all().aggregate(Min('views_count')) ['views_count__min']
    commentWithLeastViews = Comment.objects.get(views_count=minViewedComment)


    ownerIdWithMostTasks =Counter(Task.objects.values_list('user', flat=True)).most_common(1).pop(0).__getitem__(0)
    ownerMostTasksNum = Counter(Task.objects.values_list('user', flat=True)).most_common(1).pop(0).__getitem__(1)
    owner = User.objects.all().filter(id=ownerIdWithMostTasks).first()


    taskIdWithMostComments = Counter(Comment.objects.values_list('task', flat=True)).most_common(1).pop(0).__getitem__(0)
    taskWithMostCommentsNum = Counter(Comment.objects.values_list('task', flat=True)).most_common(1).pop(0).__getitem__(1)
    mostCommentedTask = Task.objects.all().filter(id=taskIdWithMostComments).first()

    ownerIdWithMostComments = Counter(Comment.objects.values_list('owner', flat=True)).most_common(1).pop(0).__getitem__(0)
    ownerWithMostCommentsNum = Counter(Comment.objects.values_list('owner', flat=True)).most_common(1).pop(0).__getitem__(1)
    ownerMostComments = User.objects.all().filter(id=ownerIdWithMostComments).first()
    return render(req, 'tasks.html', {'tasks': allTasks ,'comments': allComments, 'avgViewsPerComment': avgCommentViewCount, 'totalComments': commentsCount,
                                      'avgCommentsPerTask': avgCommentPerTask, 'mostViewedComment': commentWithMostViews, 'leastViewedComment': commentWithLeastViews,
                                      'ownerMostTasks': owner, 'taskMostComments': mostCommentedTask, 'ownerMostComments': ownerMostComments,
                                      'ownerMostTasksNum': ownerMostTasksNum, 'taskMostCommentsNum': taskWithMostCommentsNum, 'ownerMostCommentsNum': ownerWithMostCommentsNum})

def task(req, id):
    thisTask = Task.objects.get(id=id)
    allComments = Comment.objects.all().filter(task=thisTask).count()
    return render(req, 'task.html', {'task': thisTask, 'comments': allComments})

@permission_required('todoList.add_task')
def newTask(req):
    if req.method =='POST':
            form = TaskForm(req.POST)

            if form.is_valid():
                a = Task(taskname = form.cleaned_data['taskname'], description = form.cleaned_data['description'],
                         category = form.cleaned_data['category'], user = req.user)
                a.save()
                return redirect('tasks')
            else:
                return render(req, 'newTask.html', {'form': form})
    else:
        form = TaskForm()

        return render(req, 'newTask.html', {'form': form})

@permission_required('todoList.change_task')
def editTask(req, id):
    if(req.method== 'POST'):
        tsk = Task.objects.get(id=id)
        form = TaskForm(req.POST, instance=tsk)
        if form.is_valid():
            tsk.taskname = form.cleaned_data['taskname']
            tsk.description = form.cleaned_data['description']
            tsk.category = form.cleaned_data['category']
            tsk.save()
            return redirect('tasks')
        else:
            return render(req, 'editTask.html', {'form': form, 'id': id})
    else:
        tsk = Task.objects.get(id=id)
        form = TaskForm(instance=tsk)
        return render(req, 'editTask.html', {'form': form, 'id': id})

@permission_required('todoList.delete_task')
def deleteTask(req, id):
    Task.objects.get(id=id).delete()
    return redirect('tasks')

def loggedOut(req):
    return render(req, 'loggedOut.html')

@permission_required('todoList.view_comment')
def showComments(req, id):
    tsk = Task.objects.get(id=id)
    allComments = Comment.objects.all().filter(task=tsk)
    if(len(allComments)!=0):
        mostViewedCommentcnt = allComments.aggregate(Max('views_count'))['views_count__max']
        mostViewedComment = allComments.get(views_count=mostViewedCommentcnt)

        leastViewedCommentcnt = allComments.aggregate(Min('views_count'))['views_count__min']
        leastViewedComment = allComments.get(views_count=leastViewedCommentcnt)
    else:
        mostViewedComment = 'Nema komentara za ovaj task'
        leastViewedComment = 'Nema komentara za ovaj task'

    commentsGT10views= len(allComments.filter(views_count__gt=10))

    return render(req, 'comments.html', {'comments': allComments, 'task': tsk, 'mostViewedComment': mostViewedComment, 'leastViewedComment': leastViewedComment
                                         , 'commentsWithMoreThan10Views': commentsGT10views})

@permission_required('todoList.add_comment')
def newComment(req, id):
    if req.method =='POST':
            tsk = Task.objects.get(id=id)
            form = CommentForm(req.POST)
            if form.is_valid():
                a = Comment(content = form.cleaned_data['content'], task = tsk, views_count= form.cleaned_data['views_count'], owner=req.user)
                a.save()
                return redirect('tasks')
            else:
                return render(req, 'newComment.html', {'form': form, 'task_id': id, 'task': tsk})
    else:
        tsk = Task.objects.get(id=id)
        form = CommentForm()

        return render(req, 'newComment.html', {'form': form, 'task_id': id, 'task': tsk})

@permission_required('todoList.change_comment')
def editComment(req, id):
    if req.method =='POST':
            com = Comment.objects.get(id=id)
            form = CommentForm(req.POST)
            if form.is_valid():
                com.content = form.cleaned_data['content']
                com.views_count = form.cleaned_data['views_count']
                com.save()
                return redirect('tasks')
            else:
                return render(req, 'editComment.html', {'form': form, 'id': id, 'comment': com})
    else:
        com = Comment.objects.get(id=id)
        form = CommentForm(instance=com)
        return render(req, 'editComment.html', {'form': form, 'id': id})

@permission_required('todoList.delete_comment')
def deleteComment(req, id):
    Comment.objects.get(id=id).delete()
    return redirect('tasks')