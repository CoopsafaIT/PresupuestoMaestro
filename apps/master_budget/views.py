import datetime as dt
import json
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.main.models import Periodo
from .models import MasterParameters
from .forms import (
    MasterParametersForm,
    MasterParametersEditForm,
)
from utils.pagination import pagination
from utils.sql import execute_sql_query


@login_required()
def master_budget_dashboard(request):
    ctx = {}
    return render(request, 'master_budget/dashboard.html', ctx)


@login_required()
def projection_parameters(request):
    form = MasterParametersForm()
    if request.is_ajax():
        year = dt.date.today().year - 1
        period = Periodo.objects.filter(descperiodo=year).first()
        query = (
            f'EXEC dbo.sp_pptoMaestroCarteraCredCatObtenerFechasCierreHist '
            f'@PeriodoId = {period.pk}'
        )
        result = execute_sql_query(query)
        data = []
        if result.get('status') == 'ok':
            for item in result.get('data'):
                date = item.get('FechaBase')
                data.append({
                    'id': f'{ date.strftime("%Y-%m-%d") }',
                    'date': f'{ date.strftime("%d/%m/%Y") }'
                })
        return HttpResponse(json.dumps(data), content_type='application/json')

    if request.method == 'POST':
        form = MasterParametersForm(request.POST)
        if not form.is_valid():
            messages.warning(
                request,
                f'Formulario no válido: {form.errors.as_text()}'
            )
        else:
            if request.POST.get('is_active') == 'True':
                MasterParameters.objects.filter(
                    period_id=request.POST.get('period_id')
                ).update(is_active=False)

            total = MasterParameters.objects.filter(
                period_id=request.POST.get('period_id')
            ).count()
            today = str(dt.date.today())
            _new = form.save()
            _new.created_by = request.user
            _new.updated_by = request.user
            _new.correlative = (
                f'PRO-{_new.period_id.descperiodo}-Num-{total + 1}-'
                f'{today.replace("-",".")}'
            )
            _new.save()
            form = MasterParametersForm()
            messages.success(
                request,
                'Parametro de proyección creado con éxito!'
            )

    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')
    period = request.GET.get('period', '')
    filters = {}
    if not not period:
        filters['period_id'] = period

    qs = MasterParameters.objects.filter(
        Q(date_base__icontains=q) |
        Q(name__icontains=q) |
        Q(period_id__descperiodo__icontains=q)
    ).filter(**filters).exclude(deleted=True)
    periods = Periodo.objects.filter(habilitado=True)
    result = pagination(qs, page)
    ctx = {
        'periods': periods,
        'result': result,
        'form': form,
    }
    return render(request, 'MB_projection_parameters/list.html', ctx)


@login_required()
def projection_parameter(request, id):
    qs = get_object_or_404(MasterParameters, pk=id)
    form = MasterParametersEditForm(instance=qs)

    if request.method == 'POST':
        if request.POST.get('method') == 'edit':
            form = MasterParametersEditForm(request.POST, instance=qs)
            if not form.is_valid():
                messages.warning(
                    request,
                    f'Formulario no válido: {form.errors.as_text()}'
                )
            else:
                if request.POST.get('is_active') == 'True':
                    MasterParameters.objects.filter(
                        period_id=qs.period_id
                    ).update(is_active=False)
                _new = form.save()
                _new.updated_by = request.user
                _new.save()
                messages.success(
                    request,
                    'Parametro de proyección editado con éxito!'
                )
        elif request.POST.get('method') == 'delete':
            qs.is_active = False
            qs.deleted = True
            qs.save()
            messages.success(
                request,
                'Parametro de proyección eliminado con éxito!'
            )
            return redirect('projection_parameters')
    ctx = {
        'form': form,
    }
    return render(request, 'MB_projection_parameters/edit.html', ctx)
