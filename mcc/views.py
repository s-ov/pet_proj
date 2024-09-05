from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import MotorControlCenter as MCC
from substation.models import Substation
from node.models import Node


def substation_mccs_view(request, substation_slug):
    substation = get_object_or_404(Substation, slug=substation_slug)
    mccs = MCC.objects.filter(substation=substation)
    
    context = {
        'substation': substation,
        'mccs': mccs
    }
    return render(request, 'mcc/substation_mccs.html', context)


def mcc_nodes_view(request, mcc_slug):
    mcc = get_object_or_404(MCC, slug=mcc_slug)
    nodes = Node.objects.filter(mcc=mcc)
    
    context = {
        'mcc': mcc, 
        'nodes': nodes
        }
    return render(request, 'mcc/mcc_detail.html', context)
