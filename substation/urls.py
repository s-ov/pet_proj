from django.urls import path
from .views import substations_list_view


app_name = 'substation'

urlpatterns = [
    path('', substations_list_view, name='substations'),
]
