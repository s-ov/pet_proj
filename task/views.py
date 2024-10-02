from django.shortcuts import render, get_object_or_404, redirect

from .models import Task
from .forms import TaskForm


def task_list_view(request):
    return render(request, 'servicing/tasks_list.html', {
        'tasks': Task.objects.all(),
        'title': 'Список завдань',
    })


def task_detail_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'servicing/task_detail.html', {
        'task': task,
    })


def create_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_page') 
    else:
        form = TaskForm()

    return render(request, 'tasks/assign_task.html', {'form': form})
