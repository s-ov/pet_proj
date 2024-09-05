from django.urls import path
from .views import SubstationsListView, substations_list_view


app_name = 'substation'

urlpatterns = [
    path('', substations_list_view, name='substations'),
    # path('', SubstationsListView.as_view(), name='substations'),
]