from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import QuerySet
from typing import Any

from substation.models import Substation
from mcc.models import MotorControlCenter as MCC


def substations_list_view(request):
    """
    Retrieve and display a list of all substations.
    
    Args:
        request (HttpRequest): The HTTP request object. It contains metadata about 
                               the request and is passed to the view function.

    Returns:
        HttpResponse: The rendered HTML page as a response, using the 'substation/base.html' 
                      template with the context containing all `Substation` objects.
    """
    substations = Substation.objects.all()
    return render(request, 'substation/base.html', {'substations': substations})
