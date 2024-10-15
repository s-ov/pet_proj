from django.urls import path
from django.contrib.auth.views import PasswordChangeDoneView

from .employee_views import ( 
    employee_register_view,
    employee_login_view,
    employee_profile_view,
    employee_update_view,
    password_change_view,
    employee_logout_view,
    delete_employee_view,
    electricians_list_view,

    employee_tasks_view
    )


app_name = 'users'

urlpatterns = [
    path('register/', employee_register_view, name='register'),
    path('login/', employee_login_view, name='login'),
    path('logout/', employee_logout_view, name='logout'),

    path('employee_profile/<int:employee_id>/', employee_profile_view, name='employee_profile'),
    path('update_profile/', employee_update_view, name='update_profile'),
    path('password_change/', password_change_view, name='password_change'),
    path(
        'password_change_done/', 
         PasswordChangeDoneView.as_view(template_name='users/registration/password_change_done.html'), 
         name='password_change_done'
         ),
    path('delete_account/', delete_employee_view, name='delete_account'),

    path('electricians/', electricians_list_view, name='electricians_list'),

    path('employee_tasks/<int:user_id>', employee_tasks_view, name='employee_tasks')

]
