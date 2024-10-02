from django.urls import path
from .views import create_task_view, tasks_list_view, task_detail_view


app_name = 'task'

urlpatterns = [
    path('create_task/', create_task_view, name='create_task'),
    path('tasks_list/', tasks_list_view, name='tasks_list'),
    path('task_detail/<int:task_pk>/', task_detail_view, name='task_detail'),
]