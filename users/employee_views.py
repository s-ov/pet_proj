from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.urls import reverse
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Employee
from .employee_forms import (
    EmployeeRegistrationForm, 
    EmployeeLoginForm, 
    EmployeeCellUpdateForm, 
    EmployeePasswordChangeForm,
    EmployeePasswordCheckForm,
    )
from task.models import UserTask


def electricians_list_view(request):
    """
    Display list of all electricians in the application.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the html page with users' list.
    """
    try:
        electricians = Employee.objects.filter(role='Electrician')
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
        'electricians': electricians,
        'page_obj': page_obj,
        'title': 'Список користувачів'
    }
    
    return render(request, 'users/electricians_list.html', context)


def employee_register_view(request):
    """
    Handle user registration.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the registration form on GET request.
                      Redirects to login page on successful POST request.
    """
    
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.set_password(form.cleaned_data['password'])
            employee.save()
            return redirect('users:login') 
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'users/registration/register.html', {'form': form})
    
    
def employee_login_view(request):
    """
    Handle user login.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the login form on GET request.
                      Redirects to user profile on successful POST request.
    """
    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            cell_number = form.cleaned_data['cell_number']
            password = form.cleaned_data['password']
            employee = authenticate(request, username=cell_number, password=password)
            if employee is not None:
                login(request, employee)
                url = reverse('users:employee_profile', kwargs={'employee_id': employee.pk})
                return redirect(url)  
            else:
                messages.error(request, 'Неправильний номер мобільного чи пароль.')
    else:
        form = EmployeeLoginForm()

    return render(request, 'users/registration/login.html', {'form': form})


@login_required
def employee_profile_view(request, employee_id):
    """
    Render the user profile page for a specific user based on user ID.

    Args:
    - request: HttpRequest object representing the request made to the view.
    - employee_id: ID of the user whose profile is being viewed.

    Returns:
    - HttpResponse object rendering the 'users/user_profile.html' template with user data.

    Raises:
    - Http404: If no user with the specified cell number exists in the database.
    """
    try:
        employee = get_object_or_404(Employee, id=employee_id)
    except Employee.DoesNotExist:
        raise Http404("Такого користувача не знайдено.")
    return render(request, 'users/employee_profile.html', {'users': [employee], 'title': 'Мій профіль'})


def employee_update_view(request):
    """
    Handle user cell number update.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the user profile update form on GET request.
                      Redirects to user profile on successful POST request.
    """
    employee = request.user
    
    if request.method == 'POST':
        form = EmployeeCellUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('users:employee_profile', employee_id=employee.id)
        else:
            messages.error(request, 'Ваші дані не вдалося оновити. Будь ласка, перевірте пароль.')
    else:
        form = EmployeeCellUpdateForm(instance=employee)
    
    return render(request, 'users/update_mobile.html', {'form': form, 'title': 'Оновити мобільний'})

    
def password_change_view(request):
    """
    Handle user password change.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the password change form on GET request.
                      Redirects to user profile on successful POST request.
    """
    if request.method == 'POST':
        form = EmployeePasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            employee = form.save()
            update_session_auth_hash(request, employee)
            
            if employee.pk:  
                return redirect(reverse('users:password_change_done'))
            else:
                messages.error(request, 'Ваш пароль не вдалося оновити.')
    else:
        form = EmployeePasswordChangeForm(request.user)
    return render(request, 'users/registration/password_change.html', {
        'form': form
    })

def employee_logout_view(request):
    """
    Handle user logout.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Redirects to home page on successful logout.
    """
    logout(request)
    return redirect(reverse('main_page'))  


def delete_employee_view(request):
    """
    Handle user account deletion.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the delete user form on GET request.
                      Redirects to home page on successful POST request.
    """
    if request.method == 'POST':
        form = EmployeePasswordCheckForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            user.delete()
            logout(request)
            messages.success(request, 'Ваш обліковий запис було видалено.')
            return redirect(reverse('users:login'))
    else:
        form = EmployeePasswordCheckForm(request.user)
    
    return render(request, 'users/delete_user.html', {'form': form, 'title': 'Видалити профіль'})


def employee_tasks_view(request, user_id):
    """
    Display a list of tasks assigned to a specific user.

    Args:
        request: The HTTP request object.
        user_id (int): The ID of the user whose tasks are to be retrieved.

    Returns:
        HttpResponse: Renders the 'users/user_tasks.html' template with the user and their tasks.

    Raises:
        Http404: If no user with the given ID is found.
    """
    user = get_object_or_404(Employee, id=user_id)
    tasks = UserTask.objects.for_user(user)
    return render(request, 'users/employee_tasks.html', {'user': user, 'tasks': tasks, 'title': 'Мої завдання'})
