from django.urls import path
from django.conf.urls import handler400, handler403, handler404, handler500
from django.contrib.auth.views import PasswordChangeDoneView

from .views import (index_view, users_view, 
                    user_register_view,
                    user_login_view,
                    user_profile_view,
                    user_update_view,
                    password_change_view,
                    user_logout_view,
                    delete_user_view,
                    bad_request, permission_denied, page_not_found, server_error,
                    )


app_name = 'users'

urlpatterns = [
    path('', index_view, name='home'),
    path('users/', users_view, name='users'),
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
]

# handler400 = bad_request
# handler403 = permission_denied
# handler404 = page_not_found
# handler500 = server_error
