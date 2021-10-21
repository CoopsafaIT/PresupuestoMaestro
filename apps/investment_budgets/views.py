import datetime as dt
import json

from django.http import HttpResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.core.exceptions import ValidationError

from apps.main.models import (
    Detallexpresupuestoinversion,
    Centrocostoxcuentacontable,
    Cuentascontables,
    Centroscosto,
    Periodo,
    ResponsablesPorCentrosCostos,
    Inversiones,
    Transaccionesinversiones,
    Historicotrasladosinversiones
)

from utils.constants import MONTHS_LIST, MONTH_CHOICES
from utils.pagination import pagination
from apps.investment_budgets.forms import InvestmentCUForm
from apps.investment_budgets.reports import create_excel_report


@login_required()
def investment_budget_register(request):
    if (
        not request.user.has_perm('ppto_inversion.puede_ingresar_ppto_inversion_todos') and
        not request.user.has_perm('ppto_inversion.puede_ingresar_ppto_inversion')
    ):
        raise PermissionDenied

    def _get_ceco():
        if not request.user.has_perm('ppto_inversion.puede_ingresar_ppto_inversion_todos'):
            ceco_assigned = ResponsablesPorCentrosCostos.objects.filter(
                CodUser=request.user.pk, Estado=True
            ).values_list('CodCentroCosto', flat=True)
            return Centroscosto.objects.filter(habilitado=True).filter(
                pk__in=list(ceco_assigned)
            )
        else:
            return Centroscosto.objects.filter(habilitado=True)
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
                investment_id = form.cleaned_data.get('investment')
                unit_amount = float(form.cleaned_data.get('unit_amount').replace(',', ''))
                total = number * unit_amount
                qs_period = Periodo.objects.get(
                    pk=form.cleaned_data.get('period')
                )
                qs_ceco_x_cta = Centrocostoxcuentacontable.objects.get(
                    codcentrocosto=form.cleaned_data.get('cost_center'),
                    codcuentacontable=form.cleaned_data.get('account')
                )
                qs_investment = get_object_or_404(
                    Inversiones, codinversion=investment_id
                )
                _new = Detallexpresupuestoinversion()
                _new.mes = form.cleaned_data.get('month')
                _new.justificacion = form.cleaned_data.get('justification')
                _new.descproducto = qs_investment.descinversion
                _new.numero_meses_depreciacion = qs_investment.meses_depreciacion
                _new.cantidad = number
                _new.valor = unit_amount
                _new.presupuestadocontraslado = total
                _new.presupuestado = total
                _new.reservado = 0
                _new.ejecutado = 0
                _new.periodo = qs_period
                _new.codcentrocostoxcuentacontable = qs_ceco_x_cta
                _new.habilitado = True
                _new.fechacreacion = dt.datetime.today()
                _new.usuariocreacion = request.user
                _new.save()
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
    accounts = Cuentascontables.objects.filter(codtipocuenta=2, habilitado=True)
    ctx = {
        'periods': periods,
        'cost_centers': _get_ceco(),
        'accounts': accounts,
        'months': MONTHS_LIST
    }
    if (
        request.session.get('period', None) and
        request.session.get('cost_center', None)
    ):
        cost_center = request.session.get('cost_center')
        ceco_filter = {}
        if cost_center != '__all__':
            ceco_filter = {
                'codcentrocostoxcuentacontable__codcentrocosto': cost_center
            }
        qs = Detallexpresupuestoinversion.objects.extra({
            'presupuestado': 'Presupuestado',
        }).filter(
            periodo=request.session.get('period'),
            habilitado=True,
            **ceco_filter
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
            investment_id = form.cleaned_data.get('investment')

            qs_investment = get_object_or_404(
                Inversiones, codinversion=investment_id
            )
            upd_record = Detallexpresupuestoinversion.objects.get(pk=id)
            upd_record.mes = form.cleaned_data.get('month')
            upd_record.justificacion = form.cleaned_data.get('justification')
            upd_record.descproducto = qs_investment.descinversion
            upd_record.numero_meses_depreciacion = qs_investment.meses_depreciacion
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
            raise e
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
    ceco_filter = {}
    if cost_center != '__all__':
        ceco_filter = {
            'codcentrocostoxcuentacontable__codcentrocosto': cost_center
        }
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
        periodo=period,
        habilitado=True,
        **ceco_filter
    ))
    return create_excel_report(qs)


@login_required
@permission_required(
    'ppto_inversion.puede_registrar_egresos_inversion', raise_exception=True
)
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


@login_required
@permission_required(
    'ppto_inversion.puede_crear_traslados_inversion', raise_exception=True
)
def transfers_investment(request):
    def get_investments_list(cost_center, period):
        qs = Detallexpresupuestoinversion.objects.extra({
            'disponible': 'CAST(CAST(Disponible as decimal (17,2)) as nvarchar(50))',
            'presupuestado': 'CAST(CAST(Presupuestado as decimal (17,2)) as nvarchar(50))',
        }
        ).values(
            'pk',
            'descproducto',
            'disponible',
            'presupuestado',
            'coddetallexpresupuesto'
        ).filter(
            codcentrocostoxcuentacontable__codcentrocosto=cost_center,
            periodo=period,
            habilitado=True
        )
        return qs

    if request.is_ajax():
        if request.method == 'GET':
            ctx = {}
            cost_center = request.GET.get('cost_center')
            period = request.GET.get('period')

            ctx['qs'] = list(get_investments_list(cost_center=cost_center, period=period))
            return HttpResponse(
                json.dumps({'data': ctx}),
                content_type='application/json'
            )
        elif request.method == 'POST':
            ctx = {}
            cost_center = request.POST.get('cost_center')
            period = request.POST.get('period')
            investment = request.POST.get('investment')
            account = request.POST.get('account')

            qs_period = get_object_or_404(Periodo, pk=period)
            qs_investment = get_object_or_404(Inversiones, pk=investment)

            month_number = dt.datetime.today().month
            month = dict(MONTH_CHOICES).get(month_number)
            justify = (
                f'Inversion ingresada en modulo de traslado. '
                f'En fecha {dt.datetime.now()}'
            )

            _new = Detallexpresupuestoinversion()
            _new.mes = month
            _new.justificacion = justify
            _new.descproducto = qs_investment.descinversion
            _new.numero_meses_depreciacion = qs_investment.meses_depreciacion
            _new.cantidad = 1
            _new.valor = 0
            _new.presupuestadocontraslado = 0
            _new.presupuestado = 0
            _new.reservado = 0
            _new.ejecutado = 0
            _new.periodo = qs_period
            _new.codcentrocostoxcuentacontable = Centrocostoxcuentacontable.objects.get(
                codcentrocosto=cost_center,
                codcuentacontable=account
            )
            _new.habilitado = True
            _new.fechacreacion = dt.datetime.today()
            _new.usuariocreacion = request.user
            _new.save()
            ctx['qs'] = list(get_investments_list(cost_center, period))
            ctx['new_record'] = _new.pk
            ctx['cost_center'] = cost_center
            return HttpResponse(
                json.dumps({'data': ctx}),
                content_type='application/json'
            )

    if request.method == 'POST':
        total_amount = float(request.POST.get('total_amount_transfer'))
        origin = json.loads(request.POST.get('origin'))
        investment_destination = request.POST.get('investment_destination')
        period = request.POST.get('period_origin')
        qs_destination = get_object_or_404(
            Detallexpresupuestoinversion,
            pk=investment_destination
        )
        qs_period = get_object_or_404(Periodo, pk=period)
        increases_in = 0
        for item in origin:
            amount = float(item.get('amount'))
            qs_origin = get_object_or_404(
                Detallexpresupuestoinversion,
                pk=item.get('id')
            )
            new_budget = float(qs_origin.presupuestadocontraslado) - amount
            qs_origin.presupuestadocontraslado = new_budget
            qs_origin.save()
            increases_in += amount

            transc = Historicotrasladosinversiones()
            transc.periodo = qs_period.pk
            transc.codorigen = qs_origin
            transc.coddestino = qs_destination
            transc.montoorigen = float(qs_origin.presupuestadocontraslado) + amount
            transc.montodestino = float(qs_destination.presupuestadocontraslado) + amount
            transc.montotraslado = amount
            transc.montoorigendespues = float(qs_origin.presupuestadocontraslado)
            transc.montodestinodespues = float(qs_destination.presupuestadocontraslado) + increases_in # NOQA
            transc.fechacreacion = dt.datetime.today()
            transc.fecha = dt.datetime.today()
            transc.save()

        total_budget = float(qs_destination.presupuestadocontraslado) + total_amount
        qs_destination.cantidad = 1
        qs_destination.valor = float(qs_destination.valor) + total_amount
        qs_destination.presupuestadocontraslado = total_budget
        qs_destination.save()
        messages.success(
            request,
            'Traslado realizado con éxito!'
        )

    if request.GET.get('cost_center') and request.GET.get('period'):
        request.session['period'] = request.GET.get('period', '')
        request.session['cost_center'] = request.GET.get('cost_center', '')

    periods = Periodo.objects.filter(habilitado=True)
    cost_centers = Centroscosto.objects.filter(habilitado=True)
    accounts = Cuentascontables.objects.filter(codtipocuenta=2, habilitado=True)
    ctx = {
        'periods': periods,
        'cost_centers': cost_centers,
        'accounts': accounts,
    }

    if (
        request.session.get('period', None) and
        request.session.get('cost_center', None)
    ):
        cost_center = request.session['cost_center']
        period = request.session['period']

        qs = Detallexpresupuestoinversion.objects.extra({
            'disponible': 'CAST(CAST(Disponible as decimal (17,2)) as nvarchar(50))',
            'presupuestado': 'CAST(CAST(Presupuestado as decimal (17,2)) as nvarchar(50))',
        },
            where=["Disponible>0"]
        ).values(
            'pk',
            'descproducto',
            'disponible',
            'presupuestado',
            'coddetallexpresupuesto'
        ).filter(
            codcentrocostoxcuentacontable__codcentrocosto=cost_center,
            periodo=period,
            habilitado=True
        )
        ctx['qs'] = qs

    return render(request, 'transfers_investment/list.html', ctx)
