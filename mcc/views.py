from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import MotorControlCenter as MCC
from substation.models import Substation
from node.models import Node


def substation_mccs_view(request, substation_slug):
    """
    Retrieve and display Motor Control Centers (MCCs) associated with a specific substation.

    Args:
        request (HttpRequest): The HTTP request object.
        substation_slug (str): The slug of the substation whose MCCs are to be displayed.

    Returns:
        HttpResponse: A rendered HTML response with the substation details and its associated MCCs.
    """
    substation = get_object_or_404(Substation, slug=substation_slug)
    mccs = MCC.objects.filter(substation=substation)
    
    context = {
        'substation': substation,
        'mccs': mccs
    }
    return render(request, 'mcc/substation_mccs.html', context)


def mcc_nodes_view(request, mcc_slug):
    """
    Retrieve and display details of a specific Motor Control Center (MCC) and its associated nodes.

    Args:
        request (HttpRequest): The HTTP request object.
        mcc_slug (str): The slug of the MCC whose details and associated nodes are to be displayed.

    Returns:
        HttpResponse: A rendered HTML response with the MCC details and its associated nodes.
    """
    mcc = get_object_or_404(MCC, slug=mcc_slug)
    nodes = Node.objects.filter(mcc=mcc)
    
    context = {
        'mcc': mcc, 
        'nodes': nodes
        }
    return render(request, 'mcc/mcc_detail.html', context)
