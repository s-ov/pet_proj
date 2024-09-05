from django.urls import path
from .views import create_node_motor_view, create_node_view, node_list_view, node_detail_view

app_name = 'node'


urlpatterns = [
    
    path('node_list/', node_list_view, name='node_list'),
    path('create_node_motor/', create_node_motor_view, name='create_node_motor'),
    path('create_node/', create_node_view, name='create_node'),
    path('node/<int:node_id>/', node_detail_view, name='node_detail'),
    # path('<int:pk>/', views.NodeDetailView.as_view(), name='node_detail'),
    # path('<int:pk>/update/', views.NodeUpdateView.as_view(), name='node_update'),
    # path('<int:pk>/delete/', views.NodeDeleteView.as_view(), name='node_delete'),
]