from django.urls import path
from .views import substation_mccs_view, mcc_nodes_view


app_name = 'mcc'

urlpatterns = [
    path('substation/<slug:substation_slug>/', substation_mccs_view, name='substation_mccs'),
    path('mcc/<slug:mcc_slug>/', mcc_nodes_view, name='mcc_detail'),
]