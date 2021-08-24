# import datetime as dt
# import json

# from django.http import HttpResponse
from django.shortcuts import (
    render,
    # redirect,
    # get_object_or_404
)
# from django.urls import reverse
from django.contrib.auth.decorators import login_required
# from django.contrib import messages

from ppto_safa.constants import STAFF_POSITIONS, MONTHS_LIST
from apps.main.models import (
    Centroscosto,
    Detallexpresupuestopersonal,
    Periodo,
    Puestos,
)
from apps.staff_budgets.reports import create_excel_report


@login_required()
def staff_budgets_register(request):
    if request.method == 'POST':
        if request.POST.get('method') == 'filter-staff-budget':
            request.session['period'] = request.POST.get('period', '')
            request.session['cost_center'] = request.POST.get('cost_center', '')

        elif request.POST.get('method') == 'create-staff-budget':
            pass

    periods = Periodo.objects.filter(habilitado=True)
    cost_centers = Centroscosto.objects.filter(habilitado=True)
    job_positions = Puestos.objects.filter(puestoestado=True)
    ctx = {
        'periods': periods,
        'cost_centers': cost_centers,
        'job_positions': job_positions,
        'staff_positions': STAFF_POSITIONS,
        'months': MONTHS_LIST,
    }
    if (
        request.session.get('period', None) and
        request.session.get('cost_center', None)
    ):
        qs = Detallexpresupuestopersonal.objects.filter(
            codcentrocosto=request.session.get('cost_center'),
            periodo=request.session.get('period')
        )
        ctx['qs'] = qs
    return render(request, 'staff_budgets_register.html', ctx)


@login_required()
def generate_excel_report(request, period, cost_center):
    qs = Detallexpresupuestopersonal.objects.values(
        'tipo',
        'mes',
        'cantidad',
        'mesfin',
        'justificacion',
        'codpuesto__descpuesto',
        'codcentrocosto__desccentrocosto',
        'periodo__descperiodo'
    ).filter(
        codcentrocosto=cost_center,
        periodo=period
    ).order_by('tipo')
    return create_excel_report(qs)
