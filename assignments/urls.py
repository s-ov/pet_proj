from django.urls import path

from .views import (
    assigned_tasks_view,
    doer_tasks_list_view,
    electricians_list_view,
    )


app_name = 'assignments'
urlpatterns = [
    path('assigned_tasks/', assigned_tasks_view, name='assigned_tasks'),
    path('electricians_list/', electricians_list_view, name='electricians_list'),
    path('doer_tasks/<int:doer_id>/', doer_tasks_list_view, name='doer_tasks_list'),
]
