from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # , permission_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from apps.main.models import (
    Centroscosto,
    Periodo,
    ResponsablesPorCentrosCostos
)
from apps.main.reports import budget_execution_report as report
from utils.sql import execute_sql_query
from utils.constants import MONTH_CHOICES


def error_403(request, exception=None):
    return render(request, 'errors/403.html', {})


def error_404(request, exception=None):
    return render(request, 'errors/404.html', {})


def error_500(request, exception=None):
    return render(request, 'errors/404.html', {})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {})


@login_required
def budget_execution_report(request):
    if (
        not request.user.has_perm('ppto_gastos.puede_ver_ppto_gastos_todos') and
        not request.user.has_perm('ppto_gastos.puede_ver_ppto_gastos')
    ):
        raise PermissionDenied

    def _get_ceco():
        if not request.user.has_perm('ppto_gastos.puede_ver_ppto_gastos_todos'):
            ceco_assigned = ResponsablesPorCentrosCostos.objects.filter(
                CodUser=request.user.pk, Estado=True
            ).values_list('CodCentroCosto', flat=True)
            return Centroscosto.objects.filter(habilitado=True).filter(
                pk__in=list(ceco_assigned)
            )
        else:
            return Centroscosto.objects.filter(habilitado=True)
    if (
        request.GET.get('period') and
        request.GET.get('cost_center') and
        request.GET.get('month')
    ):
        period = request.GET.get('period')
        cost_center = request.GET.get('cost_center')
        month = request.GET.get('month')
        query = (
            f"EXEC [dbo].[EjecucionPresupuestariaXCentroCosto2] {period}, "
            f"{month}, {cost_center}"
        )
        result = execute_sql_query(query)
        if result.get('status') == 'ok':
            return report(result.get('data'))
        else:
            messages.warning(
                request, f"No se pudo crear reporte error: {result.get('data')}"
            )
            return report([])

    periods = Periodo.objects.filter(habilitado=True)
    ctx = {
        'periods': periods,
        'cost_centers': _get_ceco(),
        'months': MONTH_CHOICES
    }
    return render(request, 'budget_execution_report.html', ctx)
