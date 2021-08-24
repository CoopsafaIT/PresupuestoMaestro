import datetime as dt
import json

from django.http import HttpResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from apps.main.models import (
    Detallexpresupuestoinversion,
    Centrocostoxcuentacontable,
    Cuentascontables,
    Centroscosto,
    Periodo,
    Inversiones,
)

from ppto_safa.constants import MONTHS_LIST
from apps.investment_budgets.forms import InvestmentCUForm
from apps.investment_budgets.reports import create_excel_report


@login_required()
def investment_budget_register(request):
    if request.method == 'POST':
        if request.POST.get('method') == 'filter-investment-budget':
            request.session['period'] = request.POST.get('period', '')
            request.session['cost_center'] = request.POST.get('cost_center', '')

        if request.POST.get('method') == 'create-investment-budget':
            try:
                request.session['period'] = request.POST.get('period', '')
                request.session['cost_center'] = request.POST.get('cost_center', '')
                form = InvestmentCUForm(request.POST)
                if not form.is_valid():
                    raise ValidationError(f'{ form.errors.as_text() }')

                number = float(form.cleaned_data.get('number'))
                unit_amount = float(form.cleaned_data.get('unit_amount').replace(',', ''))
                total = number * unit_amount
                new_record = Detallexpresupuestoinversion()
                new_record.mes = form.cleaned_data.get('month')
                new_record.justificacion = form.cleaned_data.get('justification')
                new_record.descproducto = form.cleaned_data.get('investment')
                new_record.cantidad = number
                new_record.valor = unit_amount
                new_record.presupuestadocontraslado = total
                new_record.presupuestado = total
                new_record.reservado = 0
                new_record.ejecutado = 0
                new_record.periodo = Periodo.objects.get(
                    pk=form.cleaned_data.get('period')
                )
                new_record.codcentrocostoxcuentacontable = Centrocostoxcuentacontable.objects.get( # NOQA
                    codcentrocosto=form.cleaned_data.get('cost_center'),
                    codcuentacontable=form.cleaned_data.get('account')
                )
                new_record.habilitado = True
                new_record.fechacreacion = dt.datetime.today()
                new_record.usuariocreacion = request.user
                new_record.save()
                messages.success(
                    request,
                    'Presupuesto de inversión creado con éxito!'
                )
            except (
                Centrocostoxcuentacontable.DoesNotExist,
                Periodo.DoesNotExist
            ) as e:
                messages.warning(
                    request,
                    f'No encontrado: {e.__str__()}'
                )
                return redirect('investment_budget_register')
            except ValidationError as e:
                messages.warning(
                    request,
                    f'Error de validacion de formulario: {e.__str__()}'
                )
                return redirect('investment_budget_register')
            except Exception as e:
                messages.error(
                    request,
                    f'Exception no determinada: {e.__str__()}'
                )
                return redirect('investment_budget_register')

    periods = Periodo.objects.filter(habilitado=True)
    cost_centers = Centroscosto.objects.filter(habilitado=True)
    accounts = Cuentascontables.objects.filter(codtipocuenta=2, habilitado=True)
    ctx = {
        'periods': periods,
        'cost_centers': cost_centers,
        'accounts': accounts,
        'months': MONTHS_LIST
    }
    if (
        request.session.get('period', None) and
        request.session.get('cost_center', None)
    ):
        qs = Detallexpresupuestoinversion.objects.extra({
            'presupuestado': 'Presupuestado',
        }).filter(
            codcentrocostoxcuentacontable__codcentrocosto=request.session.get('cost_center'), # NOQA
            periodo=request.session.get('period'),
            habilitado=True
        )
        qs_sum = qs.extra({
            'total_budget': 'SUM(Presupuestado)',
            'amount_available': 'SUM(Disponible)'
        }).values('amount_available', 'total_budget')
        amount_available = qs_sum[0].get('amount_available', 0)
        total_budget = qs_sum[0].get('total_budget', 0)
        ctx['qs'] = qs
        ctx['amount_available'] = amount_available
        ctx['total_budget'] = total_budget
    return render(request, 'investment_budgets_register.html', ctx)


@login_required()
def investment_budget_update(request, id):
    if request.method == 'POST':
        try:
            request.session['period'] = request.POST.get('period', '')
            request.session['cost_center'] = request.POST.get('cost_center', '')
            form = InvestmentCUForm(request.POST)
            if not form.is_valid():
                raise ValidationError(f'{ form.errors.as_text() }')

            number = float(form.cleaned_data.get('number'))
            unit_amount = float(form.cleaned_data.get('unit_amount').replace(',', ''))
            total = number * unit_amount
            upd_record = Detallexpresupuestoinversion.objects.get(pk=id)
            upd_record.mes = form.cleaned_data.get('month')
            upd_record.justificacion = form.cleaned_data.get('justification')
            upd_record.descproducto = form.cleaned_data.get('investment')
            upd_record.cantidad = number
            upd_record.valor = unit_amount
            upd_record.presupuestadocontraslado = total
            upd_record.presupuestado = total
            upd_record.periodo = Periodo.objects.get(
                pk=form.cleaned_data.get('period')
            )
            upd_record.codcentrocostoxcuentacontable = Centrocostoxcuentacontable.objects.get( # NOQA
                codcentrocosto=form.cleaned_data.get('cost_center'),
                codcuentacontable=form.cleaned_data.get('account')
            )
            upd_record.save()
            messages.success(
                request,
                'Presupuesto de inversión editado con éxito!'
            )
            return redirect('investment_budget_register')
        except (
            Centrocostoxcuentacontable.DoesNotExist,
            Periodo.DoesNotExist,
            Detallexpresupuestoinversion.DoesNotExist
        ) as e:
            messages.warning(
                request,
                f'No encontrado: {e.__str__()}'
            )
            return redirect(reverse('investment_budget_update', kwargs={'id': id}))
        except ValidationError as e:
            messages.warning(
                request,
                f'Error de validacion de formulario: {e.__str__()}'
            )
            return redirect(reverse('investment_budget_update', kwargs={'id': id}))
        except Exception as e:
            messages.error(
                request,
                f'Exception no determinada: {e.__str__()}'
            )
            return redirect(reverse('investment_budget_update', kwargs={'id': id}))
    else:
        qs = get_object_or_404(Detallexpresupuestoinversion, pk=id)
        periods = Periodo.objects.filter(habilitado=True)
        cost_centers = Centroscosto.objects.filter(habilitado=True)
        accounts = Cuentascontables.objects.filter(codtipocuenta=2, habilitado=True)
        investments = Inversiones.objects.values(
            'codinversion',
            'descinversion'
        ).filter(
            codcuentacontable=qs.codcentrocostoxcuentacontable.codcuentacontable.pk,
            Habilitado=True
        )
        ctx = {
            'qs': qs,
            'periods': periods,
            'cost_centers': cost_centers,
            'accounts': accounts,
            'investments': investments,
            'months': MONTHS_LIST
        }
        return render(request, 'investment_budget_update.html', ctx)


@login_required()
def investement_budget_delete(request, id):
    if request.method == 'POST':
        Detallexpresupuestoinversion.objects.filter(pk=id).update(habilitado=False)
        messages.success(
            request,
            'Presupuesto de inversión eliminado con éxito'
        )
        return redirect('investment_budget_register')


@login_required()
def get_investment_by_account(request, account_id):
    if request.is_ajax():
        data = Inversiones.objects.values(
            'codinversion',
            'descinversion'
        ).filter(
            codcuentacontable=account_id,
            Habilitado=True
        )
        return HttpResponse(json.dumps(list(data)), content_type='application/json')


@login_required()
def generate_excel_report(request, period, cost_center):
    qs = list(Detallexpresupuestoinversion.objects.values(
        'codcentrocostoxcuentacontable__codcentrocosto__desccentrocosto',
        'codcentrocostoxcuentacontable__codcuentacontable__desccuentacontable',
        'periodo__descperiodo',
        'mes',
        'descproducto',
        'cantidad',
        'valor',
        'justificacion',
        'presupuestado'
    ).filter(
        codcentrocostoxcuentacontable__codcentrocosto=cost_center,
        periodo=period,
        habilitado=True
    ))
    return create_excel_report(qs)
