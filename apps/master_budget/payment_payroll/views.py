import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
# from django.db.models import Q, Sum
from decimal import Decimal as dc

from apps.main.models import Detallexpresupuestopersonal, Centroscosto
from apps.master_budget.models import MasterParameters
from utils.constants import STATUS_SCENARIO, MONTH
from utils.pagination import pagination
from utils.sql import execute_sql_query
from .models import (
    PaymentPayrollScenario,
    BudgetedPaymentPayroll,
    PaymentPayroll
)
from .forms import PaymentPayrollScenarioForm
from .request_get import QueryGetParms


@login_required()
def scenarios_payment_payroll(request):
    form = PaymentPayrollScenarioForm()

    def _monthly_salary(cost_center, acumulated=0, month=1, type=2):
        keys_start = [x for x in range(1, month+1)]
        keys_exclude = [x for x in range(1, month)]
        months = [MONTH.get(key) for key in keys_start]
        months_exclude = [MONTH.get(key) for key in keys_exclude]
        if type == 2:
            permanent = 0
            qs_staff_perm = Detallexpresupuestopersonal.objects.filter(
                periodo=_new.period_id.pk,
                codcentrocosto=cost_center.pk,
                mes__in=months,
                tipo=2
            ).values('codpuesto__sueldopermanente', 'cantidad')
            for budget in qs_staff_perm:
                salary = budget.get('codpuesto__sueldopermanente', 0)
                total = salary * budget.get('cantidad')
                permanent = permanent + total
            return permanent + acumulated

        elif type == 1:
            temp = 0
            qs_staff_temp = Detallexpresupuestopersonal.objects.filter(
                periodo=_new.period_id.pk,
                codcentrocosto=cost_center.pk,
                mes__in=months,
                tipo=1
            ).exclude(mesfin__in=months_exclude).values(
                'codpuesto__sueldotemporal', 'cantidad'
            )

            for budget in qs_staff_temp:
                salary = budget.get('codpuesto__sueldotemporal', 0)
                total = salary * budget.get('cantidad')
                temp = temp + total
            return temp

    def _add_budgeted(qs_scenario, data):
        for staff in data:
            if not BudgetedPaymentPayroll.objects.filter(
                scenario_id=qs_scenario.pk,
                budgeted_id=staff.pk
            ).exists():
                BudgetedPaymentPayroll.objects.create(
                    scenario_id=qs_scenario,
                    budgeted_id=staff
                )

    def _correlative(period, total):
        return f'ESC-{period}-{total}'

    if request.method == 'POST':
        if request.POST.get('method') == 'create':
            form = PaymentPayrollScenarioForm(request.POST)
            if not form.is_valid():
                messages.warning(
                    request,
                    f'Formulario no válido: {form.errors.as_text()}'
                )
            else:
                if request.POST.get('is_active') == 'True':
                    PaymentPayrollScenario.objects.filter(
                        parameter_id=request.POST.get('parameter_id')
                    ).update(is_active=False)
                _new = form.save()
                _new.period_id = _new.parameter_id.period_id
                _new.created_by = request.user
                _new.updated_by = request.user
                _new.save()
                _new.correlative = _correlative(
                    _new.parameter_id.period_id.descperiodo,
                    PaymentPayrollScenario.objects.filter(
                        period_id=_new.period_id
                    ).count()
                )
                _new.save()
                messages.success(
                    request,
                    'Escenario creado con éxito!'
                )
                qs_budgeted = Detallexpresupuestopersonal.objects.filter(
                    periodo=_new.period_id.pk
                )
                _add_budgeted(_new, qs_budgeted)
                result = execute_sql_query(
                    (
                        f"EXEC [dbo].[sp_pptoMaestroPlanillasObtenerSaldoHist] "
                        f"@ParametroId = {_new.parameter_id.pk}"
                    )
                )
                if result.get('status') == 'ok':
                    for item in result.get('data'):
                        qs_cost_center = get_object_or_404(
                            Centroscosto, codigocentrocosto=item.get('CENTRO_COSTO')
                        )
                        _new_detail = PaymentPayroll()
                        _new_detail.scenario_id = _new
                        _new_detail.cost_center_id = qs_cost_center
                        _new_detail.permanent_amount_initial = item.get('SueldoPermanente')
                        _new_detail.adjusted_permanent_amount = item.get('SueldoPermanente') # NOQA
                        _new_detail.amount_initial_temp = item.get('SueldoContrato')
                        _new_detail.amount_january = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 1) # NOQA
                        _new_detail.amount_february = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 2) # NOQA
                        _new_detail.amount_march = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 3) # NOQA
                        _new_detail.amount_april = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 4) # NOQA
                        _new_detail.amount_may = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 5) # NOQA
                        _new_detail.amount_june = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 6) # NOQA
                        _new_detail.amount_july = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 7) # NOQA
                        _new_detail.amount_august = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 8) # NOQA
                        _new_detail.amount_september = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 9) # NOQA
                        _new_detail.amount_october = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 10) # NOQA
                        _new_detail.amount_november = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 11) # NOQA
                        _new_detail.amount_december = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 12) # NOQA
                        _new_detail.amount_temp_january = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 1, 1) # NOQA
                        _new_detail.amount_temp_february = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 2, 1) # NOQA
                        _new_detail.amount_temp_march = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 3, 1) # NOQA
                        _new_detail.amount_temp_april = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 4, 1) # NOQA
                        _new_detail.amount_temp_may = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 5, 1) # NOQA
                        _new_detail.amount_temp_june = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 6, 1) # NOQA
                        _new_detail.amount_temp_july = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 7, 1) # NOQA
                        _new_detail.amount_temp_august = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 8, 1) # NOQA
                        _new_detail.amount_temp_september = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 9, 1) # NOQA
                        _new_detail.amount_temp_october = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 10, 1) # NOQA
                        _new_detail.amount_temp_november = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 11, 1) # NOQA
                        _new_detail.amount_temp_december = _monthly_salary(qs_cost_center, item.get('SueldoPermanente'), 12, 1) # NOQA
                        _new_detail.save()
                else:
                    messages.danger(
                        request, 'No se pudo extraer información Historica'
                    )

                redirect_url = reverse(
                    'scenario_non_performing_assets', kwargs={'id': _new.pk}
                )
                full_redirect_url = f'{redirect_url}?option='
                return redirect(full_redirect_url)

    query_parms = QueryGetParms(request.GET)
    qs = PaymentPayrollScenario.objects.filter(**query_parms.get_query_filters()).exclude(
        deleted=True
    ).order_by(
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
    return render(request, 'payment_payroll/scenarios.html', ctx)


@login_required()
def scenario_payment_payroll(request, id):
    qs = get_object_or_404(PaymentPayrollScenario, pk=id)

    def _monthly_salary(budgeted_list, acumulated=0, month=1, type=2):
        keys_start = [x for x in range(1, month+1)]
        keys_exclude = [x for x in range(1, month)]
        months = [MONTH.get(key) for key in keys_start]
        months_exclude = [MONTH.get(key) for key in keys_exclude]
        if type == 2:
            permanent = 0
            qs_staff_perm = Detallexpresupuestopersonal.objects.filter(
                pk__in=budgeted_list,
                mes__in=months,
                tipo=2
            ).values('codpuesto__sueldopermanente', 'cantidad')
            for budget in qs_staff_perm:
                salary = budget.get('codpuesto__sueldopermanente', 0)
                total = salary * budget.get('cantidad')
                permanent = permanent + total
            return permanent + acumulated

        elif type == 1:
            temp = 0
            qs_staff_temp = Detallexpresupuestopersonal.objects.filter(
                pk__in=budgeted_list,
                mes__in=months,
                tipo=1
            ).exclude(mesfin__in=months_exclude).values(
                'codpuesto__sueldotemporal', 'cantidad'
            )

            for budget in qs_staff_temp:
                salary = budget.get('codpuesto__sueldotemporal', 0)
                total = salary * budget.get('cantidad')
                temp = temp + total
            return temp

    if request.method == 'POST':
        if request.POST.get('method') == 'change-ceco-amount':
            adjusted_amount = dc(request.POST.get('adjusted_amount').replace(',', ''))
            _update = get_object_or_404(PaymentPayroll, pk=request.POST.get('pk'))
            last_amount = _update.adjusted_permanent_amount
            different = adjusted_amount - last_amount
            _update.adjusted_permanent_amount = adjusted_amount
            _update.amount_january = _update.amount_january + different
            _update.amount_february = _update.amount_february + different
            _update.amount_march = _update.amount_march + different
            _update.amount_april = _update.amount_april + different
            _update.amount_may = _update.amount_may + different
            _update.amount_june = _update.amount_june + different
            _update.amount_july = _update.amount_july + different
            _update.amount_august = _update.amount_august + different
            _update.amount_september = _update.amount_september + different
            _update.amount_october = _update.amount_october + different
            _update.amount_november = _update.amount_november + different
            _update.amount_december = _update.amount_december + different
            _update.save()
            messages.success(request, "Actualización realizada con éxito.")

        elif request.POST.get('method') == 'edit-budgeted':
            remove = json.loads(request.POST.get('remove', '[]'))
            add = json.loads(request.POST.get('add', '[]'))
            if remove:
                for item in remove:
                    qs_item = BudgetedPaymentPayroll.objects.get(
                        scenario_id=qs.pk, budgeted_id=item
                    )
                    qs_cost_center = qs_item.budgeted_id.codcentrocosto
                    type_staff = qs_item.budgeted_id.tipo
                    qs_item.delete()
                    qs_row = PaymentPayroll.objects.filter(
                        scenario_id=qs.pk, cost_center_id=qs_cost_center.pk
                    ).first()
                    if type_staff == 2:
                        budgeted_permanent = list(BudgetedPaymentPayroll.objects.filter(
                            scenario_id=qs.pk, budgeted_id__tipo=2,
                            budgeted_id__codcentrocosto=qs_cost_center
                        ).values_list('budgeted_id', flat=True))
                        initial_amount = qs_row.adjusted_permanent_amount
                        qs_row.amount_january = _monthly_salary(budgeted_permanent, initial_amount, 1) # NOQA
                        qs_row.amount_february = _monthly_salary(budgeted_permanent, initial_amount, 2) # NOQA
                        qs_row.amount_march = _monthly_salary(budgeted_permanent, initial_amount, 3) # NOQA
                        qs_row.amount_april = _monthly_salary(budgeted_permanent, initial_amount, 4) # NOQA
                        qs_row.amount_may = _monthly_salary(budgeted_permanent, initial_amount, 5) # NOQA
                        qs_row.amount_june = _monthly_salary(budgeted_permanent, initial_amount, 6) # NOQA
                        qs_row.amount_july = _monthly_salary(budgeted_permanent, initial_amount, 7) # NOQA
                        qs_row.amount_august = _monthly_salary(budgeted_permanent, initial_amount, 8) # NOQA
                        qs_row.amount_september = _monthly_salary(budgeted_permanent, initial_amount, 9) # NOQA
                        qs_row.amount_october = _monthly_salary(budgeted_permanent, initial_amount, 10) # NOQA
                        qs_row.amount_november = _monthly_salary(budgeted_permanent, initial_amount, 11) # NOQA
                        qs_row.amount_december = _monthly_salary(budgeted_permanent, initial_amount, 12) # NOQA
                        qs_row.save()

                    elif type_staff == 1:
                        budgeted_temp = list(BudgetedPaymentPayroll.objects.filter(
                            scenario_id=qs.pk, budgeted_id__tipo=1,
                            budgeted_id__codcentrocosto=qs_cost_center
                        ).values_list('budgeted_id', flat=True))
                        qs_row.amount_temp_january = _monthly_salary(budgeted_temp, 0, 1, 1) # NOQA
                        qs_row.amount_temp_february = _monthly_salary(budgeted_temp, 0, 2, 1) # NOQA
                        qs_row.amount_temp_march = _monthly_salary(budgeted_temp, 0, 3, 1)
                        qs_row.amount_temp_april = _monthly_salary(budgeted_temp, 0, 4, 1)
                        qs_row.amount_temp_may = _monthly_salary(budgeted_temp, 0, 5, 1)
                        qs_row.amount_temp_june = _monthly_salary(budgeted_temp, 0, 6, 1)
                        qs_row.amount_temp_july = _monthly_salary(budgeted_temp, 0, 7, 1)
                        qs_row.amount_temp_august = _monthly_salary(budgeted_temp, 0, 8, 1)
                        qs_row.amount_temp_september = _monthly_salary(budgeted_temp, 0, 9, 1) # NOQA
                        qs_row.amount_temp_october = _monthly_salary(budgeted_temp, 0, 10, 1) # NOQA
                        qs_row.amount_temp_november = _monthly_salary(budgeted_temp, 0, 11, 1) # NOQA
                        qs_row.amount_temp_december = _monthly_salary(budgeted_temp, 0, 12, 1) # NOQA
                        qs_row.save()

            if add:
                for item in add:
                    qs_staff = Detallexpresupuestopersonal.objects.get(pk=item)
                    qs_item = BudgetedPaymentPayroll()
                    qs_item.scenario_id = qs
                    qs_item.budgeted_id = qs_staff
                    qs_item.save()
                    qs_cost_center = qs_item.budgeted_id.codcentrocosto
                    type_staff = qs_item.budgeted_id.tipo
                    qs_row = PaymentPayroll.objects.filter(
                        scenario_id=qs.pk, cost_center_id=qs_cost_center.pk
                    ).first()
                    if type_staff == 2:
                        budgeted_permanent = list(BudgetedPaymentPayroll.objects.filter(
                            scenario_id=qs.pk, budgeted_id__tipo=2,
                            budgeted_id__codcentrocosto=qs_cost_center
                        ).values_list('budgeted_id', flat=True))
                        initial_amount = qs_row.adjusted_permanent_amount
                        qs_row.amount_january = _monthly_salary(budgeted_permanent, initial_amount, 1) # NOQA
                        qs_row.amount_february = _monthly_salary(budgeted_permanent, initial_amount, 2) # NOQA
                        qs_row.amount_march = _monthly_salary(budgeted_permanent, initial_amount, 3) # NOQA
                        qs_row.amount_april = _monthly_salary(budgeted_permanent, initial_amount, 4) # NOQA
                        qs_row.amount_may = _monthly_salary(budgeted_permanent, initial_amount, 5) # NOQA
                        qs_row.amount_june = _monthly_salary(budgeted_permanent, initial_amount, 6) # NOQA
                        qs_row.amount_july = _monthly_salary(budgeted_permanent, initial_amount, 7) # NOQA
                        qs_row.amount_august = _monthly_salary(budgeted_permanent, initial_amount, 8) # NOQA
                        qs_row.amount_september = _monthly_salary(budgeted_permanent, initial_amount, 9) # NOQA
                        qs_row.amount_october = _monthly_salary(budgeted_permanent, initial_amount, 10) # NOQA
                        qs_row.amount_november = _monthly_salary(budgeted_permanent, initial_amount, 11) # NOQA
                        qs_row.amount_december = _monthly_salary(budgeted_permanent, initial_amount, 12) # NOQA
                        qs_row.save()
                    elif type_staff == 1:
                        budgeted_temp = list(BudgetedPaymentPayroll.objects.filter(
                            scenario_id=qs.pk, budgeted_id__tipo=1,
                            budgeted_id__codcentrocosto=qs_cost_center
                        ).values_list('budgeted_id', flat=True))
                        qs_row.amount_temp_january = _monthly_salary(budgeted_temp, 0, 1, 1) # NOQA
                        qs_row.amount_temp_february = _monthly_salary(budgeted_temp, 0, 2, 1) # NOQA
                        qs_row.amount_temp_march = _monthly_salary(budgeted_temp, 0, 3, 1)
                        qs_row.amount_temp_april = _monthly_salary(budgeted_temp, 0, 4, 1)
                        qs_row.amount_temp_may = _monthly_salary(budgeted_temp, 0, 5, 1)
                        qs_row.amount_temp_june = _monthly_salary(budgeted_temp, 0, 6, 1)
                        qs_row.amount_temp_july = _monthly_salary(budgeted_temp, 0, 7, 1)
                        qs_row.amount_temp_august = _monthly_salary(budgeted_temp, 0, 8, 1)
                        qs_row.amount_temp_september = _monthly_salary(budgeted_temp, 0, 9, 1) # NOQA
                        qs_row.amount_temp_october = _monthly_salary(budgeted_temp, 0, 10, 1) # NOQA
                        qs_row.amount_temp_november = _monthly_salary(budgeted_temp, 0, 11, 1) # NOQA
                        qs_row.amount_temp_december = _monthly_salary(budgeted_temp, 0, 12, 1) # NOQA
                        qs_row.save()

    details = PaymentPayroll.objects.filter(scenario_id=id)
    budgeted = Detallexpresupuestopersonal.objects.filter(
        periodo=qs.period_id.pk
    )
    qs_budgeted_for_scenario = BudgetedPaymentPayroll.objects.filter(
        scenario_id=id
    ).values_list('budgeted_id', flat=True)

    ctx = {
        'qs': qs,
        'details': details,
        'budgeted': budgeted,
        'qs_budgeted_for_scenario': qs_budgeted_for_scenario
    }
    return render(request, 'payment_payroll/scenario.html', ctx)
