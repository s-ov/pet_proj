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
import logging

from .models import CustomUser
from .forms import (UserRegistrationForm, 
                    UserLoginForm, 
                    UserCellUpdateForm, 
                    UserPasswordChangeForm,
                    UserPasswordCheckForm,
                    )


def index_view(request):
    users = CustomUser.objects.all()
    return render(request, 'users/index.html', {'users': users})


def users_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    users = CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'users/index.html', {'users': users})


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
                # return redirect(reverse('users:user_profile', kwargs={'user_id': user.pk}))
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
    return redirect(reverse('users:home'))  

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


def bad_request(request, exception):
    """
    Handle HTTP 400 Bad Request error and render a custom 400 error page.

    Args:
        request (HttpRequest): The HTTP request object that triggered the error.
        exception (Exception): The exception that caused the error.

    Returns:
        HttpResponse: An HTTP response object rendering the custom 400 error page with
                      a 400 status code.
    """
    return render(request, 'users/errors/400.html', status=400)

def permission_denied(request, exception):
    """
    Handle HTTP 403 Forbidden error and render a custom 403 error page.

    Args:
        request (HttpRequest): The HTTP request object that triggered the error.
        exception (Exception): The exception that caused the error.

    Returns:
        HttpResponse: An HTTP response object rendering the custom 403 error page with
                      a 403 status code.
    """
    return render(request, 'users/errors/403.html', status=403)

def page_not_found(request, exception):
    """
    Handle HTTP 404 Not Found error and render a custom 404 error page.

    Args:
        request (HttpRequest): The HTTP request object that triggered the error.
        exception (Exception): The exception that caused the error.

    Returns:
        HttpResponse: An HTTP response object rendering the custom 404 error page with
                      a 404 status code.
    """
    return render(request, 'users/errors/404.html', status=404)

def server_error(request):
    """
    Handle HTTP 500 Internal Server Error and render a custom 500 error page.

    Args:
        request (HttpRequest): The HTTP request object that triggered the error.

    Returns:
        HttpResponse: An HTTP response object rendering the custom 500 error page with
                      a 500 status code.
    """
    return render(request, 'users/errors/500.html', status=500)
