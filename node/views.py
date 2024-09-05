from django.shortcuts import render, redirect

from .forms import NodeCreationForm, NodeMotorCreationForm
from .models import Node, NodeMotor


def node_list_view(request):
    nodes = Node.objects.all()
    return render(request, 'node/node_list.html', {'nodes': nodes})


def create_node_motor_view(request):
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
    if request.method == 'POST':
        form = NodeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('node:node_list')  
    else:
        form = NodeCreationForm()

    return render(request, 'node/create_node.html', {'form': form})


def node_detail_view(request, node_id):
    node = Node.objects.get(id=node_id)
    motor = node.motor

    context = {
        'node': node,
        'motor': motor
    }
    return render(request, 'node/node_detail.html', context)

