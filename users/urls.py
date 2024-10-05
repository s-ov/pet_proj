from django.urls import path
from django.contrib.auth.views import PasswordChangeDoneView

from .views import ( 
    user_register_view,
    user_login_view,
    user_profile_view,
    user_update_view,
    password_change_view,
    user_logout_view,
    delete_user_view,
    electricians_list_view,

    user_tasks_view
    )


app_name = 'users'

urlpatterns = [
    path('register/', user_register_view, name='register'),
    path('login/', user_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),

    path('user_profile/<int:user_id>/', user_profile_view, name='user_profile'),
    path('update_profile/', user_update_view, name='update_profile'),
    path('password_change/', password_change_view, name='password_change'),
    path(
        'password_change_done/', 
         PasswordChangeDoneView.as_view(template_name='users/registration/password_change_done.html'), 
         name='password_change_done'
         ),
    path('delete_account/', delete_user_view, name='delete_account'),

    path('electricians/', electricians_list_view, name='electricians_list'),

    path('user_tasks/<int:user_id>', user_tasks_view, name='user_tasks')

]
