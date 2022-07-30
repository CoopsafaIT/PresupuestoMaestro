from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.master_budget.models import MasterParameters
from apps.master_budget.patrimony import forms
from apps.master_budget.patrimony.request_get import QueryGetParms
from apps.master_budget.patrimony.request_post import equity_monthly_amount_clean
from apps.master_budget.patrimony.models import EquityCategory, EquityScenario, Equity
from utils.constants import STATUS_SCENARIO, OTHERS_ASSETS_CRITERIA
from utils.sql import execute_sql_query
from utils.pagination import pagination


@login_required()
def scenarios_equity(request):
    form = forms.EquityScenarioForm()

    def _correlative(period, total):
        return f'ESC-{period}-{total}'

    if request.POST:
        if request.POST.get('method') == 'create':
            form = forms.EquityScenarioForm(request.POST)
            if not form.is_valid():
                messages.warning(request, f'Formulario no válido: {form.errors.as_text()}')
            else:
                if request.POST.get('is_active') == 'True':
                    EquityScenario.objects.filter(
                        parameter_id=request.POST.get('parameter_id')
                    ).update(is_active=False)
                _new = form.save()
                _new.period_id = _new.parameter_id.period_id
                _new.created_by = request.user
                _new.updated_by = request.user
                _new.save()
                _new.correlative = _correlative(
                    _new.parameter_id.period_id.descperiodo,
                    EquityScenario.objects.filter(
                        period_id=_new.period_id
                    ).count()
                )
                _new.save()
                messages.success(request, 'Escenario creado con éxito!')
                for qs_category in EquityCategory.objects.filter(is_active=True):
                    query = f"{qs_category.identifier} '{_new.parameter_id.pk}'"
                    result = execute_sql_query(query)
                    if result.get('status') == 'ok':
                        for item in result.get('data'):
                            Equity.objects.create(
                                scenario_id=_new,
                                category_id=qs_category,
                                category=item.get('CategoriaId', 0),
                                category_name=item.get('Categoria', ''),
                                previous_balance=item.get('Saldo', 0),
                                percentage=0,
                                new_balance=0,
                                amount_january=item.get('Saldo', 0),
                                amount_february=item.get('Saldo', 0),
                                amount_march=item.get('Saldo', 0),
                                amount_april=item.get('Saldo', 0),
                                amount_may=item.get('Saldo', 0),
                                amount_june=item.get('Saldo', 0),
                                amount_july=item.get('Saldo', 0),
                                amount_august=item.get('Saldo', 0),
                                amount_september=item.get('Saldo', 0),
                                amount_october=item.get('Saldo', 0),
                                amount_november=item.get('Saldo', 0),
                                amount_december=item.get('Saldo', 0)
                            )
                    else:
                        messages.danger(
                            request, f'No se pudo extraer información Historica de categoria: {qs_category}' # NOQA
                        )
                redirect_url = reverse('scenario_equity', kwargs={'id': _new.pk})
                full_redirect_url = f'{redirect_url}?option='
                return redirect(full_redirect_url)
        elif request.POST.get('method') == 'clone':
            id = request.POST.get('id')
            comment = request.POST.get('comment')
            is_active = request.POST.get('is_active')
            qs_old_esc = get_object_or_404(EquityScenario, pk=id)
            _clone = EquityScenario.objects.get(pk=id)
            _clone.pk = None
            _clone.save()
            if is_active == 'True':
                EquityScenario.objects.filter(
                    parameter_id=_clone.parameter_id.pk
                ).update(is_active=False)
            _clone.comment = comment
            _clone.is_active = is_active
            _clone.created_by = request.user
            _clone.updated_by = request.user
            _clone.correlative = _correlative(
                _clone.parameter_id.period_id.descperiodo,
                EquityScenario.objects.filter(period_id=_clone.period_id).count()
            )
            _clone.save()
            _clone.refresh_from_db()
            for item_category in Equity.objects.filter(scenario_id=qs_old_esc.pk):
                _new = Equity.objects.get(pk=item_category.pk)
                _new.pk = None
                _new.save()
                _new.scenario_id = _clone
                _new.save()
            messages.success(request, 'Escenario clonado con éxito!')
            redirect_url = reverse(
                'scenario_equity', kwargs={'id': _clone.pk}
            )
            full_redirect_url = f'{redirect_url}?option='
            return redirect(full_redirect_url)

    query_parms = QueryGetParms(request.GET)
    filters = query_parms.get_query_filters()
    qs = EquityScenario.objects.filter(**filters).exclude(deleted=True).order_by(
        '-parameter_id__is_active', 'correlative'
    )
    parameters = MasterParameters.objects.filter(is_active=True).order_by(
        '-is_active', 'period_id'
    )
    result = pagination(qs, page=query_parms.get_page())
    ctx = {
        'parameters': parameters,
        'status': STATUS_SCENARIO,
        'result': result,
        'form': form
    }
    return render(request, 'equity/scenarios.html', ctx)


@login_required()
def scenario_equity(request, id):
    qs = get_object_or_404(EquityScenario, pk=id)
    if request.method == 'POST':
        if request.POST.get('method') == 'criteria':
            item = get_object_or_404(Equity, pk=request.POST.get('pk'))
            item.comment = request.POST.get('comment', '')
            item.percentage = request.POST.get('percentage').replace(',', '')
            item.new_balance = request.POST.get('new_balance').replace(',', '')
            item.criteria = request.POST.get('criteria')
            item.save()
            messages.success(request, "Actualización realizada con éxito!")
        elif request.POST.get('method') == 'define-monthly-by-amount':
            qs_item = get_object_or_404(Equity, pk=request.POST.get('pk'))
            data = equity_monthly_amount_clean(request.POST)
            form = forms.EquityDefineAmountMonthlyForm(data, instance=qs_item)
            if not form.is_valid():
                messages.warning(request, f'Formulario no válido: {form.errors.as_text()}')
            else:
                Equity.objects.filter(pk=qs_item.pk).update(**form.cleaned_data)
                messages.success(request, "Actualización realizada con éxito!")
        elif request.POST.get('method') == 'change-status':
            if not qs.is_active:
                EquityScenario.objects.filter(
                    parameter_id=qs.parameter_id.pk
                ).update(is_active=False)
            qs.is_active = not qs.is_active
            qs.save()
            message = (
                f'Escenario actualizado a : '
                f'{"Principal" if qs.is_active else "Secundario"}'
                f' con éxito!!'
            )
            messages.success(request, message)
        elif request.POST.get('method') == 'delete':
            qs.is_active = False
            qs.deleted = True
            qs.updated_by = request.user
            qs.save()
            messages.error(request, 'Escenario eliminado')
            return redirect('scenarios_others_passives')

    qs_details = Equity.objects.filter(scenario_id=qs.pk).order_by(
        'category_id', 'category'
    )
    ctx = {
        'qs': qs,
        'qs_details': qs_details,
        'others_assets_criteria': OTHERS_ASSETS_CRITERIA,
        'form_clone': forms.ScenarioCloneForm()
    }
    return render(request, 'equity/scenario.html', ctx)
