from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from users.models import Employee
from .models import TaskAssignment


def assigned_tasks_view(request):
    """View to display all tasks."""
    assigned_tasks = TaskAssignment.objects.all()
    context ={'assigned_tasks': assigned_tasks, 'title': 'Завдання',}

    return render(request, 'assignments/assigned_tasks.html', context,)


def electricians_list_view(request):
    """
    View to display all doers.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
    Returns:
        HttpResponse: Renders the HTML page with a list of doerі.
    """
    try:
        electricians = Employee.objects.filter(role='Electrician').order_by('last_name')
        paginator = Paginator(electricians, 2)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except PageNotAnInteger:
        page_obj = paginator.page(1)

    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    except Employee.DoesNotExist:
        page_obj = None

    context = {
        'page_obj': page_obj,
        'title': 'Співробітники',
        'default_message': 'Співробітників не знайдено.',
    }
    return render(request, 'assignments/electricians_list.html', context,)


def doer_tasks_list_view(request, doer_id):
    """
    View to display all tasks assigned to a specific doer (employee).

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        doer_id (int): The ID of the doer (employee) whose tasks should be retrieved.

    Returns:
        HttpResponse: Renders the HTML page with a list of tasks for the specific doer.
    """
    try:
        doer = get_object_or_404(Employee, id=doer_id)
        tasks = TaskAssignment.objects.filter(doer=doer).select_related('task', 'node')
        paginator = Paginator(tasks, 2)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except PageNotAnInteger:
        page_obj = paginator.page(1)

    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    except Employee.DoesNotExist:
        page_obj = None

    context = {
        'doer': doer,
        'page_obj': page_obj,
        'title': 'Завдання',
        'default_message': 'Співробітнику завдань не поставлено.'
    }
    return render(request, 'assignments/doer_tasks_list.html', context)
