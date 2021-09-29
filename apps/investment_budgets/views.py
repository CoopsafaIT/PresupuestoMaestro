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
from django.db.models import Sum, Q
from django.core.exceptions import ValidationError

from apps.main.models import (
    Detallexpresupuestoinversion,
    Centrocostoxcuentacontable,
    Cuentascontables,
    Centroscosto,
    Periodo,
    Inversiones,
    Transaccionesinversiones,

)

from utils.constants import MONTHS_LIST
from utils.pagination import pagination
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


@login_required
def check_out_investment(request):
    if request.is_ajax():
        if request.GET.get('method') == 'reserve':
            require_number = (
                f'{Transaccionesinversiones.objects.all().count()}'
                f'{dt.datetime.now().year}{dt.datetime.now().month}'
            )
            return HttpResponse(
                json.dumps({'require_number': require_number}),
                content_type='application/json'
            )
        elif request.GET.get('method') == 'require':
            id = request.GET.get('id', '')
            comments = Transaccionesinversiones.objects.values('comentario').filter(
                coddetallexpresupuestoinversion=id
            )
            settlement_number = (
                f'{Transaccionesinversiones.objects.all().count()}'
                f'{dt.datetime.now().year}{dt.datetime.now().month}'
                f'{Transaccionesinversiones.objects.all().count()}'
            )
            sql_statement = 'CONVERT(nvarchar(25), CAST(Comprometido as DECIMAL(23,2)))'
            requests = Transaccionesinversiones.objects.extra({
                'comprometido': sql_statement,
            }).values('numerosolicitud', 'comprometido', 'pk').filter(
                numeroliquidacion__isnull=True, coddetallexpresupuestoinversion=id
            )
            data = {
                'comments': list(comments),
                'settlement_number': settlement_number,
                'requests': list(requests),
            }
            return HttpResponse(json.dumps(data), content_type='application/json')

    if request.method == 'POST':
        if request.POST.get('method') == 'reserve':
            qs = get_object_or_404(Detallexpresupuestoinversion, pk=request.POST.get('id'))
            qs.reservado = float(qs.reservado) + float(request.POST.get('amount_reserve'))
            qs.usuariomodificacion = request.user
            qs.fechamodificacion = dt.datetime.today()
            qs.save()

            transaction = Transaccionesinversiones()
            transaction.comprometido = float(request.POST.get('amount_reserve'))
            transaction.coddetallexpresupuestoinversion = qs
            transaction.fechacreacion = request.POST.get('request_date')
            transaction.numerosolicitud = request.POST.get('correlative_reserve')
            transaction.usuariocreacion = request.user.pk
            transaction.save()
            messages.success(request, 'Reserva realizada con éxito!')

        elif request.POST.get('method') == 'require':
            qs = get_object_or_404(Detallexpresupuestoinversion, pk=request.POST.get('id'))
            if request.POST.get('request_number') == 'not_request_number':
                amount = float(request.POST.get('purchase_amount'))
                available = Detallexpresupuestoinversion.objects.extra(
                    {'disponible': 'Disponible'}
                ).values('disponible').get(pk=qs.pk)
                if amount > float(available.get('disponible')):
                    messages.warning(
                        request,
                        (
                            f'Requisición de compra por valor {amount} '
                            f'mayor al disponible: {float(available.get("disponible"))}'
                        )
                    )
                    return redirect('check_out_investment')

                trans = Transaccionesinversiones()
                trans.coddetallexpresupuestoinversion = qs
                trans.requerido = request.POST.get('purchase_amount')
                trans.numeroliquidacion = request.POST.get('settlement_number')
                trans.usuariocreacion = request.user.pk
                trans.fechacreacion = dt.datetime.today()
                trans.comentario = request.POST.get('comment')
                trans.save()

                executed = Transaccionesinversiones.objects.filter(
                    coddetallexpresupuestoinversion=trans.coddetallexpresupuestoinversion
                ).aggregate(Sum('requerido'))

                qs.comentario = request.POST.get('comment')
                qs.ejecutado = float(executed.get('requerido__sum'))
                qs.save()

            else:
                id_trans = request.POST.get('request_number')
                qs_trans = get_object_or_404(Transaccionesinversiones, pk=id_trans)
                amount_trans_reserve = qs_trans.comprometido
                amount_trans_require = qs_trans.requerido
                correlative_number = qs_trans.numerosolicitud
                purchase_amount = float(request.POST.get('purchase_amount'))
                if amount_trans_require is None:
                    amount_available = float(amount_trans_reserve)
                else:
                    amount_available = float(amount_trans_reserve) - float(amount_trans_require) # NOQA

                if purchase_amount > amount_available:
                    messages.warning(
                        request,
                        (
                            f'Requisición de compra por valor {purchase_amount} '
                            f'mayor al disponible {amount_available} para '
                            f'número de solicitud: {correlative_number}'
                        )
                    )
                    return redirect('check_out_investment')

                qs_trans.requerido = purchase_amount
                qs_trans.numeroliquidacion = request.POST.get('settlement_number')
                qs_trans.save()

                trans = Transaccionesinversiones()
                trans.coddetallexpresupuestoinversion = qs
                trans.requerido = purchase_amount
                trans.numeroliquidacion = request.POST.get('settlement_number')
                trans.usuariocreacion = request.user.pk
                trans.fechacreacion = dt.datetime.today()
                trans.comentario = request.POST.get('comment')
                trans.save()

                qs.ejecutado = float(qs.ejecutado) + purchase_amount
                qs.reservado = qs.reservado - qs_trans.comprometido
                qs.usuariomodificacion = request.user
                qs.fechamodificacion = dt.datetime.today()
                qs.save()

            messages.success(request, 'Requisición de compra realizada con éxito!')

    if request.GET.get('period') and request.GET.get('cost_center'):
        request.session['period'] = request.GET.get('period', '')
        request.session['cost_center'] = request.GET.get('cost_center', '')

    periods = Periodo.objects.filter(habilitado=True)
    cost_centers = Centroscosto.objects.filter(habilitado=True)
    ctx = {
        'periods': periods,
        'cost_centers': cost_centers
    }
    if (
        request.session.get('period', None) and
        request.session.get('cost_center', None)
    ):
        cost_center = request.session['cost_center']
        period = request.session['period']
        page = request.GET.get('page', 1)
        q = request.GET.get('q', '')
        qs = Detallexpresupuestoinversion.objects.extra({
            'presupuestado': 'CAST(CAST(Presupuestado as DECIMAL(23,5)) as nvarchar(150))',
            'reservado': 'CAST(CAST(Reservado as DECIMAL(23,5)) as nvarchar(150))',
            'ejecutado': 'CAST(CAST(Ejecutado as DECIMAL(23,5)) as nvarchar(150))',
            'disponible': 'Disponible',
        }).values(
            'pk',
            'presupuestadocontraslado',
            'reservado',
            'ejecutado',
            'disponible',
            'presupuestado',
            'periodo__descperiodo',
            'descproducto',
            'valor',
            'cantidad',
            'presupuestado',
            'tipoaccion__descripciontipoaccion',
            'tipoaccion',
            'valorfusion',
            'mes'
        ).filter(
            codcentrocostoxcuentacontable__codcentrocosto=cost_center,
            periodo=period,
            habilitado=True
        ).filter(
            Q(descproducto__icontains=q) |
            Q(cantidad__icontains=q)
        ).order_by('descproducto', 'cantidad')

        totales = qs.aggregate(
            presupuestado=Sum('presupuestadocontraslado'),
            reservado=Sum('reservado'),
            ejecutado=Sum('ejecutado')
        )

        total_available = Detallexpresupuestoinversion.objects.extra(
            {'disponible': 'SUM(Disponible)'}
        ).values('disponible').filter(
            codcentrocostoxcuentacontable__codcentrocosto=cost_center,
            periodo=period,
            habilitado=True
        )
        ctx['qs'] = pagination(qs, page=page)
        ctx['total_executed'] = totales.get('ejecutado', '')
        ctx['total_reserved'] = totales.get('reservado', '')
        ctx['total_budget'] = totales.get('presupuestado', '')
        ctx['total_available'] = total_available[0].get('disponible', '')
    return render(request, 'check_out_investment/list.html', ctx)
