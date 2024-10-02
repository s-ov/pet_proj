from django.urls import path
from django.views.generic import TemplateView 

from .views import (
                    create_node_motor_view, 
                    create_node_view, 
                    show_created_node_view,
                    show_created_node_motor_view,

                    nodes_list_view, 
                    motors_list_view,
                    node_detail_view,

                    search_node_view,
                    get_level_nodes_view,
                    
                    pre_change_data_view,
                    
                    update_node_motor_view,
                    update_node_view,

                    delete_motor_view,
                    delete_node_view,
                    )

app_name = 'node'


urlpatterns = [
    
    path('node_list/', nodes_list_view, name='node_list'),
    path('motor_list/', motors_list_view, name='motors_list'),

    path('create_node_motor/', create_node_motor_view, name='create_node_motor'),
    path('create_node/', create_node_view, name='create_node'),

    path('show_created_node/', show_created_node_view, name='show_created_node'),
    path('show_created_node_motor/', show_created_node_motor_view, name='show_created_node_motor'),

    path('get_level_nodes/', get_level_nodes_view, name='get_level_nodes'),

    path('node/<int:node_id>/', node_detail_view, name='node_detail'),
    path('pre_change_data/', pre_change_data_view, name='pre_change_data'),

    path('search_node/', search_node_view, name='search_node'),
    path('update_motor/', update_node_motor_view, name='update_motor'),
    path('update_node/', update_node_view, name='update_node'),
    path(
        'updated_motor_message/', 
         TemplateView.as_view(template_name='node/messages/updated_node_message.html'), 
         name='updated_motor_message'
         ),
    path(
        'updated_node_message/', 
         TemplateView.as_view(template_name='node/messages/updated_node_message.html'), 
         name='updated_node_message'
         ),

    path('delete_motor/', delete_motor_view, name='delete_motor'),
    path('delete_node/', delete_node_view, name='delete_node'),
    path(
        'deleted_motor_message/', 
         TemplateView.as_view(template_name='node/messages/deleted_motor_message.html'), 
         name='deleted_motor_message'
         ),
    path(
        'deleted_node_message/', 
         TemplateView.as_view(template_name='node/messages/deleted_node_message.html'), 
         name='deleted_node_message'
         ),
]