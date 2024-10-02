from django.urls import reverse
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


def user_info(request):
    """
    Add user information to the context.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        dict: A dictionary containing the user information.
    """
    if request.user.is_authenticated:
        user = CustomUser.objects.get(id=request.user.id)

        return {
            'user_profile_url': reverse('users:user_profile', kwargs={'user_id': request.user.id}),
            'user_logout_url': reverse('users:logout'),
            'user_info': user,
        }
    return {
        'user_register_url': reverse('users:register'),
        'user_login_url': reverse('users:login'),
    }
