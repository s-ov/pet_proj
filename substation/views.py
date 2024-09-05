from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import QuerySet
from typing import Any

from substation.models import Substation
from mcc.models import MotorControlCenter as MCC


def substations_list_view(request):
    substations = Substation.objects.all()
    return render(request, 'substation/base.html', {'substations': substations})

class SubstationsListView(ListView):
    # template_name = 'substation/base.html'
    # context_object_name = 'substations'
    # title_page = 'Гoлoвна'

    # def get_queryset(self) -> QuerySet[Any]:
    #     return Substation.objects.all()
    pass
