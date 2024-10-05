from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import CustomUser
from .forms import (UserRegistrationForm, 
                    UserLoginForm, 
                    UserCellUpdateForm, 
                    UserPasswordChangeForm,
                    UserPasswordCheckForm,
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
        electricians = CustomUser.objects.filter(role='Electrician')
        paginator = Paginator(electricians, 2)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except PageNotAnInteger:
        page_obj = paginator.page(1)

    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    except CustomUser.DoesNotExist:
        page_obj = None

    context = {
        'electricians': electricians,
        'page_obj': page_obj,
    }
    
    return render(request, 'users/electricians_list.html', context)


def user_register_view(request):
    """
    Handle user registration.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the registration form on GET request.
                      Redirects to login page on successful POST request.
    """
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('users:login') 
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration/register.html', {'form': form})
    
    
def user_login_view(request):
    """
    Handle user login.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the login form on GET request.
                      Redirects to user profile on successful POST request.
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cell_number = form.cleaned_data['cell_number']
            password = form.cleaned_data['password']
            user = authenticate(request, username=cell_number, password=password)
            if user is not None:
                login(request, user)
                url = reverse('users:user_profile', kwargs={'user_id': user.pk})
                return redirect(url)  
            else:
                messages.error(request, 'Неправильний номер мобільного чи пароль.')
    else:
        form = UserLoginForm()

    return render(request, 'users/registration/login.html', {'form': form})


@login_required
def user_profile_view(request, user_id):
    """
    Render the user profile page for a specific user based on user ID.

    Args:
    - request: HttpRequest object representing the request made to the view.
    - user_id: ID of the user whose profile is being viewed.

    Returns:
    - HttpResponse object rendering the 'users/user_profile.html' template with user data.

    Raises:
    - Http404: If no user with the specified cell number exists in the database.
    """
    try:
        user = get_object_or_404(CustomUser, id=user_id)
    except CustomUser.DoesNotExist:
        raise Http404("Такого користувача не знайдено.")
    return render(request, 'users/user_profile.html', {'users': [user]})


@login_required
def user_update_view(request):
    """
    Handle user cell number update.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the user profile update form on GET request.
                      Redirects to user profile on successful POST request.
    """
    user = request.user
    
    if request.method == 'POST':
        form = UserCellUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:user_profile', user_id=user.id)
        else:
            messages.error(request, 'Ваші дані не вдалося оновити. Будь ласка, перевірте пароль.')
    else:
        form = UserCellUpdateForm(instance=user)
    
    return render(request, 'users/update_profile.html', {'form': form})

    
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
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            
            if user.pk:  
                return redirect(reverse('users:password_change_done'))
            else:
                messages.error(request, 'Ваш пароль не вдалося оновити.')
    else:
        form = UserPasswordChangeForm(request.user)
    return render(request, 'users/registration/password_change.html', {
        'form': form
    })

def user_logout_view(request):
    """
    Handle user logout.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Redirects to home page on successful logout.
    """
    logout(request)
    return redirect(reverse('main_page'))  

@login_required
def delete_user_view(request):
    """
    Handle user account deletion.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the delete user form on GET request.
                      Redirects to home page on successful POST request.
    """
    if request.method == 'POST':
        form = UserPasswordCheckForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            user.delete()
            logout(request)
            messages.success(request, 'Ваш обліковий запис було видалено.')
            return redirect(reverse('users:login'))
    else:
        form = UserPasswordCheckForm(request.user)
    
    return render(request, 'users/delete_user.html', {'form': form})


def user_tasks_view(request, user_id):
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
    user = get_object_or_404(CustomUser, id=user_id)
    tasks = UserTask.objects.for_user(user)
    return render(request, 'users/user_tasks.html', {'user': user, 'tasks': tasks})
