import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from decimal import Decimal as dc

from apps.main.models import Detallexpresupuestopersonal, Centroscosto
from apps.master_budget.models import MasterParameters
from utils.constants import STATUS_SCENARIO, MONTH
from utils.pagination import pagination
from utils.sql import execute_sql_query, execute_sql_query_no_return
from .models import (
    PaymentPayrollScenario, BudgetedPaymentPayroll, PaymentPayroll
)
from .forms import (
    PaymentPayrollScenarioForm, CollateralPaymentScenarioForm
)
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
                periodo=_new.period_id.pk, codcentrocosto=cost_center.pk,
                mes__in=months, tipo=2
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
                scenario_id=qs_scenario.pk, budgeted_id=staff.pk
            ).exists():
                BudgetedPaymentPayroll.objects.create(
                    scenario_id=qs_scenario, budgeted_id=staff
                )

    def _correlative(period, total):
        return f'ESC-{period}-{total}'

    if request.method == 'POST':
        if request.POST.get('method') == 'create':
            form = PaymentPayrollScenarioForm(request.POST)
            if not form.is_valid():
                messages.warning(
                    request, f'Formulario no válido: {form.errors.as_text()}'
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
                messages.success(request, 'Escenario creado con éxito!')
                qs_budgeted = Detallexpresupuestopersonal.objects.filter(
                    periodo=_new.period_id.pk
                )
                _add_budgeted(_new, qs_budgeted)
                result = execute_sql_query(
                    "EXEC [dbo].[sp_pptoMaestroPlanillasObtenerSaldoHist]"
                )
                if result.get('status') == 'ok':
                    for item in result.get('data'):
                        qs_cost_center = get_object_or_404(
                            Centroscosto, codigocentrocosto=item.get('CENTRO_COSTO')
                        )
                        _new_detail = PaymentPayroll()
                        _new_detail.scenario_id = _new
                        _new_detail.cost_center_id = qs_cost_center
                        _new_detail.permanent_staff_number = item.get('CantidadPermanentes') # NOQA
                        _new_detail.permanent_amount_initial = item.get('SueldoPermanentes') # NOQA
                        _new_detail.adjusted_permanent_amount = item.get('SueldoPermanentes') # NOQA
                        _new_detail.temp_staff_number = item.get('CantidadPorContrato')
                        _new_detail.amount_initial_temp = item.get('SueldoPorContrato')

                        _new_detail.amount_january = _monthly_salary(qs_cost_center, item.get('SueldoPermanentes'), 1) # NOQA
                        _new_detail.amount_february = _monthly_salary(qs_cost_center, item.get('SueldoPermanentes'), 2) # NOQA
                        _new_detail.amount_march = _monthly_salary(qs_cost_center, item.get('SueldoPermanentes'), 3) # NOQA
                        _new_detail.amount_april = _monthly_salary(qs_cost_center, item.get('SueldoPermanentes'), 4) # NOQA
                        _new_detail.amount_may = _monthly_salary(qs_cost_center, item.get('SueldoPermanentes'), 5) # NOQA
                        _new_detail.amount_june = _monthly_salary(qs_cost_center, item.get('SueldoPermanentes'), 6) # NOQA
                        _new_detail.amount_july = _monthly_salary(qs_cost_center, item.get('SueldoPermanentes'), 7) # NOQA
                        _new_detail.amount_august = _monthly_salary(qs_cost_center, item.get('SueldoPermanentes'), 8) # NOQA
                        _new_detail.amount_september = _monthly_salary(qs_cost_center, item.get('SueldoPermanentes'), 9) # NOQA
                        _new_detail.amount_october = _monthly_salary(qs_cost_center, item.get('SueldoPermanentes'), 10) # NOQA
                        _new_detail.amount_november = _monthly_salary(qs_cost_center, item.get('SueldoPermanentes'), 11) # NOQA
                        _new_detail.amount_december = _monthly_salary(qs_cost_center, item.get('SueldoPermanentes'), 12) # NOQA

                        _new_detail.amount_temp_january = _monthly_salary(qs_cost_center, 0, 1, 1) # NOQA
                        _new_detail.amount_temp_february = _monthly_salary(qs_cost_center, 0, 2, 1) # NOQA
                        _new_detail.amount_temp_march = _monthly_salary(qs_cost_center, 0, 3, 1) # NOQA
                        _new_detail.amount_temp_april = _monthly_salary(qs_cost_center, 0, 4, 1) # NOQA
                        _new_detail.amount_temp_may = _monthly_salary(qs_cost_center, 0, 5, 1) # NOQA
                        _new_detail.amount_temp_june = _monthly_salary(qs_cost_center, 0, 6, 1) # NOQA
                        _new_detail.amount_temp_july = _monthly_salary(qs_cost_center, 0, 7, 1) # NOQA
                        _new_detail.amount_temp_august = _monthly_salary(qs_cost_center, 0, 8, 1) # NOQA
                        _new_detail.amount_temp_september = _monthly_salary(qs_cost_center, 0, 9, 1) # NOQA
                        _new_detail.amount_temp_october = _monthly_salary(qs_cost_center, 0, 10, 1) # NOQA
                        _new_detail.amount_temp_november = _monthly_salary(qs_cost_center, 0, 11, 1) # NOQA
                        _new_detail.amount_temp_december = _monthly_salary(qs_cost_center, 0, 12, 1) # NOQA
                        _new_detail.save()
                else:
                    messages.danger(request, 'No se pudo extraer información Historica')
                redirect_url = reverse('scenario_payment_payroll', kwargs={'id': _new.pk})
                full_redirect_url = f'{redirect_url}?option='
                return redirect(full_redirect_url)

    query_parms = QueryGetParms(request.GET)
    qs = PaymentPayrollScenario.objects.filter(**query_parms.get_query_filters()).exclude(
        deleted=True
    ).order_by('-parameter_id__is_active', 'correlative')
    parameters = MasterParameters.objects.filter(is_active=True).order_by(
        '-is_active', 'period_id'
    )
    result = pagination(qs, page=query_parms.get_page())
    ctx = {
        'parameters': parameters, 'status': STATUS_SCENARIO,
        'result': result, 'form': form
    }
    return render(request, 'payment_payroll/scenarios.html', ctx)


@login_required()
def scenario_payment_payroll(request, id):
    qs = get_object_or_404(PaymentPayrollScenario, pk=id)

    def _permanent_monthly_updated_calculation(qs_item, budgeted_permanent):
        initial_amount = qs_item.adjusted_permanent_amount
        qs_item.amount_january = _monthly_salary(budgeted_permanent, initial_amount, 1) # NOQA
        qs_item.amount_february = _monthly_salary(budgeted_permanent, initial_amount, 2) # NOQA
        qs_item.amount_march = _monthly_salary(budgeted_permanent, initial_amount, 3) # NOQA
        qs_item.amount_april = _monthly_salary(budgeted_permanent, initial_amount, 4) # NOQA
        qs_item.amount_may = _monthly_salary(budgeted_permanent, initial_amount, 5) # NOQA
        qs_item.amount_june = _monthly_salary(budgeted_permanent, initial_amount, 6) # NOQA
        qs_item.amount_july = _monthly_salary(budgeted_permanent, initial_amount, 7) # NOQA
        qs_item.amount_august = _monthly_salary(budgeted_permanent, initial_amount, 8) # NOQA
        qs_item.amount_september = _monthly_salary(budgeted_permanent, initial_amount, 9) # NOQA
        qs_item.amount_october = _monthly_salary(budgeted_permanent, initial_amount, 10) # NOQA
        qs_item.amount_november = _monthly_salary(budgeted_permanent, initial_amount, 11) # NOQA
        qs_item.amount_december = _monthly_salary(budgeted_permanent, initial_amount, 12) # NOQA
        qs_item.save()

    def _temporary_monthly_updated_calculation(qs_item, budgeted_temp):
        qs_item.amount_temp_january = _monthly_salary(budgeted_temp, 0, 1, 1) # NOQA
        qs_item.amount_temp_february = _monthly_salary(budgeted_temp, 0, 2, 1) # NOQA
        qs_item.amount_temp_march = _monthly_salary(budgeted_temp, 0, 3, 1)
        qs_item.amount_temp_april = _monthly_salary(budgeted_temp, 0, 4, 1)
        qs_item.amount_temp_may = _monthly_salary(budgeted_temp, 0, 5, 1)
        qs_item.amount_temp_june = _monthly_salary(budgeted_temp, 0, 6, 1)
        qs_item.amount_temp_july = _monthly_salary(budgeted_temp, 0, 7, 1)
        qs_item.amount_temp_august = _monthly_salary(budgeted_temp, 0, 8, 1)
        qs_item.amount_temp_september = _monthly_salary(budgeted_temp, 0, 9, 1) # NOQA
        qs_item.amount_temp_october = _monthly_salary(budgeted_temp, 0, 10, 1) # NOQA
        qs_item.amount_temp_november = _monthly_salary(budgeted_temp, 0, 11, 1) # NOQA
        qs_item.amount_temp_december = _monthly_salary(budgeted_temp, 0, 12, 1) # NOQA
        qs_item.save()

    def _permanent_percentage_ceco_calculation(qs_item, qs_per):
        qs_item.amount_january = qs_item.amount_january + (
            qs_item.amount_january * dc(qs_per.percentage_increase_january) / 100
        )
        qs_item.amount_february = qs_item.amount_february + (
            qs_item.amount_february * dc(qs_per.percentage_increase_february) / 100
        )
        qs_item.amount_march = qs_item.amount_march + (
            qs_item.amount_march * dc(qs_per.percentage_increase_march) / 100
        )
        qs_item.amount_april = qs_item.amount_april + (
            qs_item.amount_april * dc(qs_per.percentage_increase_april) / 100
        )
        qs_item.amount_may = qs_item.amount_may + (
            qs_item.amount_may * dc(qs_per.percentage_increase_may) / 100
        )
        qs_item.amount_june = qs_item.amount_june + (
            qs_item.amount_june * dc(qs_per.percentage_increase_june) / 100
        )
        qs_item.amount_july = qs_item.amount_july + (
            qs_item.amount_july * dc(qs_per.percentage_increase_july) / 100
        )
        qs_item.amount_august = qs_item.amount_august + (
            qs_item.amount_august * dc(qs_per.percentage_increase_august) / 100
        )
        qs_item.amount_september = qs_item.amount_september + (
            qs_item.amount_september * dc(qs_per.percentage_increase_september) / 100
        )
        qs_item.amount_october = qs_item.amount_october + (
            qs_item.amount_october * dc(qs_per.percentage_increase_october) / 100
        )
        qs_item.amount_november = qs_item.amount_november + (
            qs_item.amount_november * dc(qs_per.percentage_increase_november) / 100
        )
        qs_item.amount_december = qs_item.amount_december + (
            qs_item.amount_december * dc(qs_per.percentage_increase_december) / 100
        )
        qs_item.save()

    def _temporary_percentage_ceco_calculation(qs_item, qs_per):
        pass
        # qs_item.amount_temp_january = qs_item.amount_temp_january + (
        #     qs_item.amount_temp_january * dc(qs_per.percentage_increase_january) / 100
        # )
        # qs_item.amount_temp_february = qs_item.amount_temp_february + (
        #     qs_item.amount_temp_february * dc(qs_per.percentage_increase_february) / 100 # NOQA
        # )
        # qs_item.amount_temp_march = qs_item.amount_temp_march + (
        #     qs_item.amount_temp_march * dc(qs_per.percentage_increase_march) / 100
        # )
        # qs_item.amount_temp_april = qs_item.amount_temp_april + (
        #     qs_item.amount_temp_april * dc(qs_per.percentage_increase_april) / 100
        # )
        # qs_item.amount_temp_may = qs_item.amount_temp_may + (
        #     qs_item.amount_temp_may * dc(qs_per.percentage_increase_may) / 100
        # )
        # qs_item.amount_temp_june = qs_item.amount_temp_june + (
        #     qs_item.amount_temp_june * dc(qs_per.percentage_increase_june) / 100
        # )
        # qs_item.amount_temp_july = qs_item.amount_temp_july + (
        #     qs_item.amount_temp_july * dc(qs_per.percentage_increase_july) / 100
        # )
        # qs_item.amount_temp_august = qs_item.amount_temp_august + (
        #     qs_item.amount_temp_august * dc(qs_per.percentage_increase_august) / 100
        # )
        # qs_item.amount_temp_september = qs_item.amount_temp_september + (
        #     qs_item.amount_temp_september * dc(qs_per.percentage_increase_september) / 100 # NOQA
        # )
        # qs_item.amount_temp_october = qs_item.amount_temp_october + (
        #     qs_item.amount_temp_october * dc(qs_per.percentage_increase_october) / 100
        # )
        # qs_item.amount_temp_november = qs_item.amount_temp_november + (
        #     qs_item.amount_temp_november * dc(qs_per.percentage_increase_november) / 100 # NOQA
        # )
        # qs_item.amount_temp_december = qs_item.amount_temp_december + (
        #     qs_item.amount_temp_december * dc(qs_per.percentage_increase_december) / 100 # NOQA
        # )
        # qs_item.save()

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
                    qs_row, created = PaymentPayroll.objects.get_or_create(
                        scenario_id=qs.pk, cost_center_id=qs_cost_center.pk
                    )
                    if type_staff == 2:
                        budgeted_permanent = list(BudgetedPaymentPayroll.objects.filter(
                            scenario_id=qs.pk, budgeted_id__tipo=2,
                            budgeted_id__codcentrocosto=qs_cost_center
                        ).values_list('budgeted_id', flat=True))
                        _permanent_monthly_updated_calculation(qs_row, budgeted_permanent)
                        qs_row.refresh_from_db()
                        _permanent_percentage_ceco_calculation(qs_row, qs)
                        qs_row.refresh_from_db()
                        _permanent_percentage_ceco_calculation(qs_row, qs_row)

                    elif type_staff == 1:
                        budgeted_temp = list(BudgetedPaymentPayroll.objects.filter(
                            scenario_id=qs.pk, budgeted_id__tipo=1,
                            budgeted_id__codcentrocosto=qs_cost_center
                        ).values_list('budgeted_id', flat=True))
                        _temporary_monthly_updated_calculation(qs_row, budgeted_temp)
                        qs_row.refresh_from_db()
                        _temporary_percentage_ceco_calculation(qs_row, qs)
                        qs_row.refresh_from_db()
                        _temporary_percentage_ceco_calculation(qs_row, qs_row)

            if add:
                for item in add:
                    qs_staff = Detallexpresupuestopersonal.objects.get(pk=item)
                    qs_item = BudgetedPaymentPayroll()
                    qs_item.scenario_id = qs
                    qs_item.budgeted_id = qs_staff
                    qs_item.save()
                    qs_cost_center = qs_item.budgeted_id.codcentrocosto
                    type_staff = qs_item.budgeted_id.tipo

                    qs_row, created = PaymentPayroll.objects.get_or_create(
                        scenario_id=qs.pk, cost_center_id=qs_cost_center.pk
                    )
                    if type_staff == 2:
                        budgeted_permanent = list(BudgetedPaymentPayroll.objects.filter(
                            scenario_id=qs.pk, budgeted_id__tipo=2,
                            budgeted_id__codcentrocosto=qs_cost_center
                        ).values_list('budgeted_id', flat=True))
                        _permanent_monthly_updated_calculation(qs_row, budgeted_permanent)
                        qs_row.refresh_from_db()
                        _permanent_percentage_ceco_calculation(qs_row, qs)
                        qs_row.refresh_from_db()
                        _permanent_percentage_ceco_calculation(qs_row, qs_row)

                    elif type_staff == 1:
                        budgeted_temp = list(BudgetedPaymentPayroll.objects.filter(
                            scenario_id=qs.pk, budgeted_id__tipo=1,
                            budgeted_id__codcentrocosto=qs_cost_center
                        ).values_list('budgeted_id', flat=True))
                        _temporary_monthly_updated_calculation(qs_row, budgeted_temp)
                        qs_row.refresh_from_db()
                        _temporary_percentage_ceco_calculation(qs_row, qs)
                        qs_row.refresh_from_db()
                        _temporary_percentage_ceco_calculation(qs_row, qs_row)


            messages.success(request, 'Actualización realizada con éxito!')

        elif request.POST.get('method') == 'edit-percentage':
            qs.percentage_increase_january = request.POST.get('percentage_increase_january').replace(',', '') # NOQA
            qs.percentage_increase_february = request.POST.get('percentage_increase_february').replace(',', '') # NOQA
            qs.percentage_increase_march = request.POST.get('percentage_increase_march').replace(',', '') # NOQA
            qs.percentage_increase_april = request.POST.get('percentage_increase_april').replace(',', '') # NOQA
            qs.percentage_increase_may = request.POST.get('percentage_increase_may').replace(',', '') # NOQA
            qs.percentage_increase_june = request.POST.get('percentage_increase_june').replace(',', '') # NOQA
            qs.percentage_increase_july = request.POST.get('percentage_increase_july').replace(',', '') # NOQA
            qs.percentage_increase_august = request.POST.get('percentage_increase_august').replace(',', '') # NOQA
            qs.percentage_increase_september = request.POST.get('percentage_increase_september').replace(',', '') # NOQA
            qs.percentage_increase_october = request.POST.get('percentage_increase_october').replace(',', '') # NOQA
            qs.percentage_increase_november = request.POST.get('percentage_increase_november').replace(',', '') # NOQA
            qs.percentage_increase_december = request.POST.get('percentage_increase_december').replace(',', '') # NOQA
            qs.save()
            qs_list = PaymentPayroll.objects.filter(scenario_id=id)
            for qs_item in qs_list:
                budgeted_permanent = list(BudgetedPaymentPayroll.objects.filter(
                    scenario_id=qs.pk, budgeted_id__tipo=2,
                    budgeted_id__codcentrocosto=qs_item.cost_center_id.pk
                ).values_list('budgeted_id', flat=True))
                budgeted_temp = list(BudgetedPaymentPayroll.objects.filter(
                    scenario_id=qs.pk, budgeted_id__tipo=1,
                    budgeted_id__codcentrocosto=qs_item.cost_center_id.pk
                ).values_list('budgeted_id', flat=True))
                _permanent_monthly_updated_calculation(qs_item, budgeted_permanent)
                _temporary_monthly_updated_calculation(qs_item, budgeted_temp)
                qs_item.refresh_from_db()
                _permanent_percentage_ceco_calculation(qs_item, qs)
                _temporary_percentage_ceco_calculation(qs_item, qs)
                qs_item.refresh_from_db()
                _permanent_percentage_ceco_calculation(qs_item, qs_item)
                _temporary_percentage_ceco_calculation(qs_item, qs_item)
                qs_item.refresh_from_db()

            messages.success(request, 'Actualización realizada con éxito!')

        elif request.POST.get('method') == 'edit-percentage-ceco':
            qs_item = PaymentPayroll.objects.filter(
                scenario_id=qs.pk, cost_center_id=request.POST.get('ceco_id')
            ).first()
            qs_item.percentage_increase_january = request.POST.get('percentage_increase_january') # NOQA
            qs_item.percentage_increase_february = request.POST.get('percentage_increase_february') # NOQA
            qs_item.percentage_increase_march = request.POST.get('percentage_increase_march') # NOQA
            qs_item.percentage_increase_april = request.POST.get('percentage_increase_april') # NOQA
            qs_item.percentage_increase_may = request.POST.get('percentage_increase_may') # NOQA
            qs_item.percentage_increase_june = request.POST.get('percentage_increase_june') # NOQA
            qs_item.percentage_increase_july = request.POST.get('percentage_increase_july') # NOQA
            qs_item.percentage_increase_august = request.POST.get('percentage_increase_august') # NOQA
            qs_item.percentage_increase_september = request.POST.get('percentage_increase_september') # NOQA
            qs_item.percentage_increase_october = request.POST.get('percentage_increase_october') # NOQA
            qs_item.percentage_increase_november = request.POST.get('percentage_increase_november') # NOQA
            qs_item.percentage_increase_december = request.POST.get('percentage_increase_december') # NOQA
            budgeted_permanent = list(BudgetedPaymentPayroll.objects.filter(
                scenario_id=qs.pk, budgeted_id__tipo=2,
                budgeted_id__codcentrocosto=qs_item.cost_center_id.pk
            ).values_list('budgeted_id', flat=True))
            budgeted_temp = list(BudgetedPaymentPayroll.objects.filter(
                scenario_id=qs.pk, budgeted_id__tipo=1,
                budgeted_id__codcentrocosto=qs_item.cost_center_id.pk
            ).values_list('budgeted_id', flat=True))
            _permanent_monthly_updated_calculation(qs_item, budgeted_permanent)
            _temporary_monthly_updated_calculation(qs_item, budgeted_temp)
            qs_item.refresh_from_db()
            _permanent_percentage_ceco_calculation(qs_item, qs)
            _temporary_percentage_ceco_calculation(qs_item, qs)
            qs_item.refresh_from_db()
            _permanent_percentage_ceco_calculation(qs_item, qs_item)
            _temporary_percentage_ceco_calculation(qs_item, qs_item)
            qs_item.refresh_from_db()
            messages.success(request, 'Actualización realizada con éxito!')

        elif request.POST.get('method') == 'change-status':
            if not qs.is_active:
                PaymentPayrollScenario.objects.filter(
                    parameter_id=qs.parameter_id.pk
                ).update(is_active=False)
            qs.is_active = not qs.is_active
            qs.save()
            message = (
                f'Escenario actualizado a : '
                f'{"Principal" if qs.is_active else "Secundario"} con éxito!!'
            )
            messages.success(request, message)

        elif request.POST.get('method') == 'delete':
            BudgetedPaymentPayroll.objects.filter(scenario_id=qs.pk).delete()
            PaymentPayroll.objects.filter(scenario_id=qs.pk).delete()
            qs.is_active = False
            qs.deleted = True
            qs.updated_by = request.user
            qs.save()
            messages.error(request, 'Escenario eliminado')
            return redirect('scenarios_payment_payroll')

        elif request.POST.get('method') == 'recalculate':
            qs_list = PaymentPayroll.objects.filter(scenario_id=id)
            for qs_item in qs_list:
                budgeted_permanent = list(BudgetedPaymentPayroll.objects.filter(
                    scenario_id=qs.pk, budgeted_id__tipo=2,
                    budgeted_id__codcentrocosto=qs_item.cost_center_id.pk
                ).values_list('budgeted_id', flat=True))
                budgeted_temp = list(BudgetedPaymentPayroll.objects.filter(
                    scenario_id=qs.pk, budgeted_id__tipo=1,
                    budgeted_id__codcentrocosto=qs_item.cost_center_id.pk
                ).values_list('budgeted_id', flat=True))
                _permanent_monthly_updated_calculation(qs_item, budgeted_permanent)
                _temporary_monthly_updated_calculation(qs_item, budgeted_temp)
                qs_item.refresh_from_db()
                _permanent_percentage_ceco_calculation(qs_item, qs)
                _temporary_percentage_ceco_calculation(qs_item, qs)
                qs_item.refresh_from_db()
                _permanent_percentage_ceco_calculation(qs_item, qs_item)
                _temporary_percentage_ceco_calculation(qs_item, qs_item)
                qs_item.refresh_from_db()

            messages.success(request, 'Recalculo realizada con éxito!')

        elif request.POST.get('method') == 'update-cta':
            form = CollateralPaymentScenarioForm(request.POST, instance=qs)
            if not form.is_valid():
                messages.warning(
                    request, f'Formulario no válido: {form.errors.as_text()}'
                )
            else:
                form.save()
                execute_sql_query_no_return(
                    f"EXEC [dbo].[sp_pptoMaestrPlanillaMigrarPresupuestoIndirecto] "
                    f"@CodPeriodo = {qs.period_id.pk} "
                )
                execute_sql_query_no_return(
                    f"EXEC [dbo].[sp_pptoMaestrPlanillaMigrarPresupuestoIndirecto"
                    f"ColateralesTreceavosCatorceavoPrestaciones] @EscenarioId = {qs.pk}"
                )
                execute_sql_query_no_return(
                    f"EXEC [dbo].[sp_pptoMasterPlanillaMigrarPresupuestoIndirecto"
                    f"ColateralesConFormula] @EscenarioId = {qs.pk}"
                )
                messages.success(request, 'Actualización realizada con éxito!')

    details = PaymentPayroll.objects.filter(scenario_id=id)
    qs_sum_perm = details.extra({
        'sum_base_perm': 'SUM(MontoPermanenteAjustado)',
        'sum_ene_perm': 'SUM(MontoEne)', 'sum_feb_perm': 'SUM(MontoFeb)',
        'sum_mar_perm': 'SUM(MontoMar)', 'sum_abr_perm': 'SUM(MontoAbr)',
        'sum_may_perm': 'SUM(MontoMay)', 'sum_jul_perm': 'SUM(MontoJun)',
        'sum_jun_perm': 'SUM(MontoJul)', 'sum_ago_perm': 'SUM(MontoAgo)',
        'sum_sep_perm': 'SUM(MontoSep)', 'sum_oct_perm': 'SUM(MontoOct)',
        'sum_nov_perm': 'SUM(MontoNov)', 'sum_dic_perm': 'SUM(MontoDic)',
    }).values(
        'sum_base_perm', 'sum_ene_perm', 'sum_feb_perm', 'sum_mar_perm',
        'sum_abr_perm', 'sum_may_perm', 'sum_jul_perm',
        'sum_jun_perm', 'sum_ago_perm', 'sum_sep_perm',
        'sum_oct_perm', 'sum_nov_perm', 'sum_dic_perm'
    )

    qs_sum_temp = details.extra({
        'sum_base_temp': 'SUM(MontoInicialTemporal)',
        'sum_ene_temp': 'SUM(MontoTemporalEne)', 'sum_feb_temp': 'SUM(MontoTemporalFeb)',
        'sum_mar_temp': 'SUM(MontoTemporalMar)', 'sum_abr_temp': 'SUM(MontoTemporalAbr)',
        'sum_may_temp': 'SUM(MontoTemporalMay)', 'sum_jul_temp': 'SUM(MontoTemporalJun)',
        'sum_jun_temp': 'SUM(MontoTemporalJul)', 'sum_ago_temp': 'SUM(MontoTemporalAgo)',
        'sum_sep_temp': 'SUM(MontoTemporalSep)', 'sum_oct_temp': 'SUM(MontoTemporalOct)',
        'sum_nov_temp': 'SUM(MontoTemporalNov)', 'sum_dic_temp': 'SUM(MontoTemporalDic)',
    }).values(
        'sum_base_temp', 'sum_ene_temp', 'sum_feb_temp', 'sum_mar_temp',
        'sum_abr_temp', 'sum_may_temp', 'sum_jul_temp',
        'sum_jun_temp', 'sum_ago_temp', 'sum_sep_temp',
        'sum_oct_temp', 'sum_nov_temp', 'sum_dic_temp'
    )
    sum_total_perm = 0
    sum_total_temp = 0
    qs_sum_perm = qs_sum_perm[0]
    qs_sum_temp = qs_sum_temp[0]
    for item, value in enumerate(qs_sum_perm):
        if value != 'sum_base_perm':
            sum_total_perm = sum_total_perm + qs_sum_perm[value]

    for item, value in enumerate(qs_sum_temp):
        if value != 'sum_base_temp':
            sum_total_temp = sum_total_temp + qs_sum_temp[value]

    budgeted = Detallexpresupuestopersonal.objects.filter(periodo=qs.period_id.pk)
    qs_budgeted_for_scenario = BudgetedPaymentPayroll.objects.filter(
        scenario_id=id
    ).values_list('budgeted_id', flat=True)
    form_update_cta = CollateralPaymentScenarioForm(instance=qs)

    ctx = {
        'qs': qs, 'details': details, 'qs_sum_perm': qs_sum_perm,
        'qs_sum_temp': qs_sum_temp, 'sum_total_perm': sum_total_perm,
        'sum_total_temp': sum_total_temp, 'form_update_cta': form_update_cta,
        'budgeted': budgeted, 'qs_budgeted_for_scenario': qs_budgeted_for_scenario
    }
    return render(request, 'payment_payroll/scenario.html', ctx)
