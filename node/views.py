from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Node, NodeMotor
from .forms import (
                    NodeCreationForm, 
                    NodeMotorCreationForm, 
                    NodeMotorForm, 
                    NodeForm,
                    NodeIndexForm,
                    NodeUpdateForm
                    )


def nodes_list_view(request):
    nodes = Node.objects.all()
    return render(request, 'node/nodes_list.html', {'nodes': nodes})


def motors_list_view(request):
    motors = NodeMotor.objects.all()
    return render(request, 'node/motors_list.html', {'motors': motors})


def create_node_motor_view(request):
    """
    Handles the creation of a new NodeMotor instance.

    Args:
        request (HttpRequest): The HTTP request object containing metadata and form data.

    Returns:
        HttpResponse: The rendered template with the form for GET requests, or a redirect 
                      to the 'node:create_node' URL after a successful form submission.
    """
    if request.method == 'POST':
        form = NodeMotorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('node:create_node')  
        else:
            print(form.errors)
    else:
        form = NodeMotorCreationForm()
    
    return render(request, 'node/create_node_motor.html', {'form': form})


def create_node_view(request):
    """
    Handles the creation of a new Node instance.

    Args:
        request (HttpRequest): The HTTP request object containing metadata and form data.

    Returns:
        HttpResponse: The rendered template with the form for GET requests, or a redirect 
                      to the 'node:node_list' URL after a successful form submission.
    """
    if request.method == 'POST':
        form = NodeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('node:node_list')  
    else:
        form = NodeCreationForm()

    return render(request, 'node/create_node.html', {'form': form})


def node_detail_view(request, node_id):
    """
    Displays the details of a specific Node instance.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        node_id (int): The ID of the Node instance to be retrieved.

    Returns:
        HttpResponse: The rendered template displaying the details of the Node and its 
                      associated NodeMotor.
    """
    node = Node.objects.get(id=node_id)
    motor = node.motor

    context = {
        'node': node,
        'motor': motor
    }
    return render(request, 'node/node_detail.html', context)


def pre_change_data_view(request):
    """
    Displays the endpoints to change the data of the NodeMotor and Node instances.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered template displaying the buttons to change the data in database.
    """
    
    return render(request, 'node/pre_change_data.html')


def update_node_motor_view(request):
    """
    Handles the NodeMotor instance updating with the provided form data.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered template displaying the updated details of the NodeMotor.
    """
    
    if request.method == 'POST':
        power = request.POST.get('power')
        
        if not power:
            return render(
                request, 
                'node/update_motor_form.html', 
                {'error': 'Введіть, буль ласка, потужність.'}
                )
        try:
            power = float(power)
            
            if 'update' in request.POST:
                motor_id = request.POST.get('motor_id')  
                motor = NodeMotor.objects.get(id=motor_id)
                form = NodeMotorForm(request.POST, instance=motor)
                
                if form.is_valid():
                    form.save()  
                    return redirect('node:motors_list')  
                else:
                    return render(
                        request, 
                        'node/update_motor_form.html', 
                        {'form': form, 'motor': motor})
            else:
                motor = NodeMotor.objects.filter(power=power).first()

                if motor is None:
                    return render(
                        request, 
                        'node/update_motor_form.html', 
                        {'error': f'Не знайдено двигун з потужністю {power}.'}
                        )

                form = NodeMotorForm(instance=motor)
                return render(
                    request, 
                    'node/update_motor_form.html', 
                    {'form': form, 'motor': motor}
                    )

        except ValueError:
            return render(
                request,
                'node/update_motor_form.html',
                {'error': 'Не правильний ввід. Введіть, буль ласка, числове значення.'}
            )

    return render(request, 'node/update_motor_form.html')


def update_node_view(request):
    """
    Handles the Node instance updating with the provided form data.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        node_id (int): The ID of the Node instance to be retrieved.

    Returns:
        HttpResponse: The rendered template displaying the updated details of the Node.
    """
