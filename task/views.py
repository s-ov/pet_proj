from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model

from .models import Task
from .forms import TaskForm

User = get_user_model()


def tasks_list_view(request):
    context = {
        'tasks': Task.objects.all(),
        'title': 'Завдання'
    }
    return render(request, 'task/tasks_list.html', context)


def task_detail_view(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    context = {
        'task': task,
        'title': 'Завдання'
    }
    return render(request, 'task/task_detail.html', context)


# def create_task_view(request):
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('task:task_detail', task_pk=form.instance.pk) 
#     else:
#         form = TaskForm()

#     return render(request, 'task/create_task.html', {'form': form})


def create_task_view(request, user_id=None):
    doer = get_object_or_404(User, id=user_id) if user_id else None

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if doer:
                task.doer = doer
            task.save()
            return redirect('task:task_detail', task_pk=form.instance.pk)
    else:
        form = TaskForm(initial={'doer': doer})

    return render(request, 'task/create_task.html', {'form': form})
