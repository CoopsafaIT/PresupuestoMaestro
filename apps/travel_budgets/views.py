import datetime as dt
import json

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q, Sum

from apps.main.models import (
    Centroscosto,
    Detallexpresupuestoviaticos,
    Filiales,
    Periodo,
    ResponsablesPorCentrosCostos,
    Manejodeviaticos,
    Transaccionesviaticos
)
from apps.travel_budgets.forms import (
    InternacionalTravelBudget,
    NacionalTravelBudget
)
from utils.constants import TRAVEL_CATEGORY, ZONES
from utils.pagination import pagination
from apps.travel_budgets.reports import (
    create_excel_report,
    generate_excel_file_format_distribution,
    load_excel_file
)


@login_required()
def travel_budget_register(request):
    if (
        not request.user.has_perm('ppto_viaticos.puede_ingresar_ppto_viaticos_todos') and
        not request.user.has_perm('ppto_viaticos.puede_ingresar_ppto_viaticos')
    ):
        raise PermissionDenied

    def _get_ceco():
        if not request.user.has_perm('ppto_viaticos.puede_ingresar_ppto_viaticos_todos'):
            ceco_assigned = ResponsablesPorCentrosCostos.objects.filter(
                CodUser=request.user.pk, Estado=True
            ).values_list('CodCentroCosto', flat=True)
            return Centroscosto.objects.filter(habilitado=True).filter(
                pk__in=list(ceco_assigned)
            )
        else:
            return Centroscosto.objects.filter(habilitado=True)

    if request.method == 'POST':
        if request.POST.get('method') == 'filter-travel-budget':
            try:
                request.session['cost_center'] = request.POST.get('cost_center', '')
                request.session['period'] = request.POST.get('period', '')
                cost_center = request.POST.get('cost_center', '')
                period = request.POST.get('period', '')
                qs_national_travel_budget = Detallexpresupuestoviaticos.objects.filter(
                    codcentrocosto=cost_center,
                    tipoviatico=1,
                    habilitado=True,
                    codperiodo=period
                )
                qs_international_travel_budget = Detallexpresupuestoviaticos.objects.filter( # NOQA
                    codcentrocosto=cost_center,
                    tipoviatico=2,
                    habilitado=True,
                    codperiodo=period
                )
            except Exception as e:
                messages.warning(request, f'Exception cached: {e.__str__() }')
            else:
                periods = Periodo.objects.filter(habilitado=True)
                filials = Filiales.objects.all()
                ctx = {
                    'periods': periods,
                    'cost_centers': _get_ceco(),
                    'filials': filials,
                    'categories': TRAVEL_CATEGORY,
                    'zones': ZONES,
                    'qs_international_travel_budget': qs_international_travel_budget,
                    'qs_national_travel_budget': qs_national_travel_budget
                }
                return render(request, 'travel_budget_register.html', ctx)

        if request.POST.get('method') == 'create-international-travel-budget':
            try:
                form = InternacionalTravelBudget(request.POST)
                if not form.is_valid():
                    raise ValidationError(f'{ form.errors.as_text() }')
                if not Detallexpresupuestoviaticos.objects.filter(
                    categoria=form.cleaned_data.get('category'),
                    zona=form.cleaned_data.get('zone'),
                    codcentrocosto=form.cleaned_data.get('cost_center'),
                    usuariocreacion=request.user.pk,
                    codperiodo=form.cleaned_data.get('period'),
                    habilitado=True
                ).exists():
                    new_record = Detallexpresupuestoviaticos()
                    new_record.codperiodo = Periodo.objects.get(
                        pk=form.cleaned_data.get('period')
                    )
                    new_record.codcentrocosto = Centroscosto.objects.get(
                        pk=form.cleaned_data.get('cost_center')
                    )
                    new_record.zona = form.cleaned_data.get('zone')
                    new_record.categoria = form.cleaned_data.get('category')
                    new_record.tipoviatico = form.cleaned_data.get('travel_type')
                    new_record.cantidadviajes = form.cleaned_data.get('number_trips')
                    new_record.cantidaddias = form.cleaned_data.get('number_days')
                    new_record.justificacion = form.cleaned_data.get('justification')
                    new_record.usuariocreacion = request.user
                    new_record.fechacreacion = dt.datetime.today()
                    new_record.habilitado = True
                    new_record.save()
                    messages.success(
                        request,
                        'Presupuesto para viatico internacional registrado con ??xito'
                    )
                else:
                    messages.warning(
                        request,
                        'Presupuesto para viatico internacional ya existe!'
                    )
            except (
                Filiales.DoesNotExist,
                Periodo.DoesNotExist,
                Centroscosto.DoesNotExist
            ) as e:
                messages.warning(
                    request,
                    f'No encontrado: {e.__str__()}'
                )
                return redirect('travel_budget_register')
            except ValidationError as e:
                messages.warning(
                    request,
                    f'Error de validacion de formulario: {e.__str__()}'
                )
                return redirect('travel_budget_register')
            except Exception as e:
                messages.error(
                    request,
                    f'Exception no determinada: {e.__str__()}'
                )
                return redirect('travel_budget_register')
            else:
                cost_center = request.POST.get('cost_center', '')
                period = request.POST.get('period', '')
                qs_national_travel_budget = Detallexpresupuestoviaticos.objects.filter(
                    codcentrocosto=cost_center,
                    tipoviatico=1,
                    habilitado=True,
                    codperiodo=period
                )
                qs_international_travel_budget = Detallexpresupuestoviaticos.objects.filter( # NOQA
                    codcentrocosto=cost_center,
                    tipoviatico=2,
                    habilitado=True,
                    codperiodo=period
                )
                periods = Periodo.objects.filter(habilitado=True)
                filials = Filiales.objects.all()
                ctx = {
                    'periods': periods,
                    'cost_centers': _get_ceco(),
                    'filials': filials,
                    'categories': TRAVEL_CATEGORY,
                    'zones': ZONES,
                    'qs_international_travel_budget': qs_international_travel_budget,
                    'qs_national_travel_budget': qs_national_travel_budget
                }
                return render(request, 'travel_budget_register.html', ctx)

        if request.POST.get('method') == 'create-national-travel-budget':
            try:
                form = NacionalTravelBudget(request.POST)
                if not form.is_valid():
                    raise ValidationError(f'{ form.errors.as_text() }')

                if not Detallexpresupuestoviaticos.objects.filter(
                    categoria=form.cleaned_data.get('category'),
                    filial=form.cleaned_data.get('filial'),
                    codcentrocosto=form.cleaned_data.get('cost_center'),
                    usuariocreacion=request.user.pk,
                    codperiodo=form.cleaned_data.get('period'),
                    habilitado=True
                ).exists():
                    new_record = Detallexpresupuestoviaticos()
                    new_record.codperiodo = Periodo.objects.get(
                        pk=form.cleaned_data.get('period')
                    )
                    new_record.filial = Filiales.objects.get(
                        pk=form.cleaned_data.get('filial')
                    )
                    new_record.categoria = form.cleaned_data.get('category')
                    new_record.tipoviatico = form.cleaned_data.get('travel_type')
                    new_record.cantidadviajes = form.cleaned_data.get('number_trips')
                    new_record.cantidaddias = form.cleaned_data.get('number_days')
                    new_record.codcentrocosto = Centroscosto.objects.get(
                        pk=form.cleaned_data.get('cost_center')
                    )
                    new_record.justificacion = form.cleaned_data.get('justification')
                    new_record.usuariocreacion = request.user
                    new_record.fechacreacion = dt.datetime.today()
                    new_record.habilitado = True
                    new_record.save()
                    messages.success(
                        request,
                        'Presupuesto para viatico nacional registrado con ??xito'
                    )
                else:
                    messages.warning(
                        request,
                        'Presupuesto para viatico nacional ya existe!'
                    )
            except (
                Filiales.DoesNotExist,
                Periodo.DoesNotExist,
                Centroscosto.DoesNotExist
            ) as e:
                messages.warning(
                    request,
                    f'No encontrado: {e.__str__()}'
                )
                return redirect('travel_budget_register')
            except ValidationError as e:
                messages.warning(
                    request,
                    f'Error de validacion de formulario: {e.__str__()}'
                )
                return redirect('travel_budget_register')
            except Exception as e:
                messages.error(
                    request,
                    f'Exception no determinada: {e.__str__()}'
                )
                return redirect('travel_budget_register')
            else:
                cost_center = request.POST.get('cost_center', '')
                period = request.POST.get('period', '')
                qs_national_travel_budget = Detallexpresupuestoviaticos.objects.filter(
                    codcentrocosto=cost_center,
                    tipoviatico=1,
                    habilitado=True,
                    codperiodo=period
                )
                qs_international_travel_budget = Detallexpresupuestoviaticos.objects.filter( # NOQA
                    codcentrocosto=cost_center,
                    tipoviatico=2,
                    habilitado=True,
                    codperiodo=period
                )
                periods = Periodo.objects.filter(habilitado=True)
                filials = Filiales.objects.all()
                ctx = {
                    'periods': periods,
                    'cost_centers': _get_ceco(),
                    'filials': filials,
                    'categories': TRAVEL_CATEGORY,
                    'zones': ZONES,
                    'qs_international_travel_budget': qs_international_travel_budget,
                    'qs_national_travel_budget': qs_national_travel_budget
                }
                return render(request, 'travel_budget_register.html', ctx)

    else:
        periods = Periodo.objects.filter(habilitado=True)
        filials = Filiales.objects.all()
        ctx = {
            'periods': periods,
            'cost_centers': _get_ceco(),
            'filials': filials,
            'categories': TRAVEL_CATEGORY,
            'zones': ZONES
        }
        if (
            request.session.get('period', None) and
            request.session.get('cost_center', None) and
            request.session.get('cost_center') != '__all__'
        ):
            qs_national_travel_budget = Detallexpresupuestoviaticos.objects.filter(
                codcentrocosto=request.session.get('cost_center'),
                tipoviatico=1,
                habilitado=True,
                codperiodo=request.session.get('period')
            )
            qs_international_travel_budget = Detallexpresupuestoviaticos.objects.filter( # NOQA
                codcentrocosto=request.session.get('cost_center'),
                tipoviatico=2,
                habilitado=True,
                codperiodo=request.session.get('period')
            )
            ctx['qs_international_travel_budget'] = qs_international_travel_budget
            ctx['qs_national_travel_budget'] = qs_national_travel_budget
        return render(request, 'travel_budget_register.html', ctx)


@login_required()
def travel_budget_update(request, id):
    if request.method == 'POST':
        if request.POST.get('method') == 'update-international-travel-budget':
            try:
                form = InternacionalTravelBudget(request.POST)
                if not form.is_valid():
                    raise ValidationError(f'{ form.errors.as_text() }')

                update_record = Detallexpresupuestoviaticos.objects.get(pk=id)
                update_record.codperiodo = Periodo.objects.get(
                    pk=form.cleaned_data.get('period')
                )
                update_record.codcentrocosto = Centroscosto.objects.get(
                    pk=form.cleaned_data.get('cost_center')
                )
                update_record.zona = form.cleaned_data.get('zone')
                update_record.categoria = form.cleaned_data.get('category')
                update_record.tipoviatico = form.cleaned_data.get('travel_type')
                update_record.cantidadviajes = form.cleaned_data.get('number_trips')
                update_record.cantidaddias = form.cleaned_data.get('number_days')
                update_record.justificacion = form.cleaned_data.get('justification')
                update_record.usuariocreacion = request.user
                update_record.fechacreacion = dt.datetime.today()
                update_record.habilitado = True
                update_record.save()
                messages.success(
                    request,
                    'Presupuesto para viatico internacional editado con ??xito'
                )
                return redirect('travel_budget_register')
            except (
                Filiales.DoesNotExist,
                Periodo.DoesNotExist,
                Centroscosto.DoesNotExist
            ) as e:
                messages.warning(
                    request,
                    f'No encontrado: {e.__str__()}'
                )
                return redirect(reverse('travel_budget_update', kwargs={'id': id}))
            except ValidationError as e:
                messages.warning(
                    request,
                    f'Error de validacion de formulario: {e.__str__()}'
                )
                return redirect(reverse('travel_budget_update', kwargs={'id': id}))
            except Exception as e:
                messages.error(
                    request,
                    f'Exception no determinada: {e.__str__()}'
                )
                return redirect(reverse('travel_budget_update', kwargs={'id': id}))

        if request.POST.get('method') == 'update-national-travel-budget':
            try:
                form = NacionalTravelBudget(request.POST)
                if not form.is_valid():
                    raise ValidationError(f'{ form.errors.as_text() }')

                update_record = Detallexpresupuestoviaticos.objects.get(pk=id)
                update_record.codperiodo = Periodo.objects.get(
                    pk=form.cleaned_data.get('period')
                )
                update_record.filial = Filiales.objects.get(
                    pk=form.cleaned_data.get('filial')
                )
                update_record.codcentrocosto = Centroscosto.objects.get(
                    pk=form.cleaned_data.get('cost_center')
                )
                update_record.categoria = form.cleaned_data.get('category')
                update_record.tipoviatico = form.cleaned_data.get('travel_type')
                update_record.cantidadviajes = form.cleaned_data.get('number_trips')
                update_record.cantidaddias = form.cleaned_data.get('number_days')
                update_record.justificacion = form.cleaned_data.get('justification')
                update_record.usuariocreacion = request.user
                update_record.fechacreacion = dt.datetime.today()
                update_record.habilitado = True
                update_record.save()
                messages.success(
                    request,
                    'Presupuesto para viatico nacional registrado con ??xito'
                )
                return redirect('travel_budget_register')
            except (
                Filiales.DoesNotExist,
                Periodo.DoesNotExist,
                Centroscosto.DoesNotExist
            ) as e:
                messages.warning(
                    request,
                    f'No encontrado: {e.__str__()}'
                )
                return redirect(reverse('travel_budget_update', kwargs={'id': id}))
            except ValidationError as e:
                messages.warning(
                    request,
                    f'Error de validacion de formulario: {e.__str__()}'
                )
                return redirect(reverse('travel_budget_update', kwargs={'id': id}))
            except Exception as e:
                messages.error(
                    request,
                    f'Exception no determinada: {e.__str__()}'
                )
                return redirect(reverse('travel_budget_update', kwargs={'id': id}))

    else:
        qs = get_object_or_404(Detallexpresupuestoviaticos, pk=id)
        periods = Periodo.objects.filter(habilitado=True)
        cost_centers = Centroscosto.objects.filter(habilitado=True)
        filials = Filiales.objects.all()
        ctx = {
            'qs': qs,
            'periods': periods,
            'cost_centers': cost_centers,
            'filials': filials,
            'categories': TRAVEL_CATEGORY,
            'zones': ZONES
        }
        return render(request, 'travel_budget_update.html', ctx)


@login_required()
def travel_budget_delete(request, id):
    if request.method == 'POST':
        Detallexpresupuestoviaticos.objects.filter(pk=id).update(habilitado=False)
        messages.success(
            request,
            'Presupuesto de viatico eliminado con ??xito'
        )
        return redirect('travel_budget_register')


@login_required()
def generate_excel_report(request, period, cost_center):
    qs = list(Detallexpresupuestoviaticos.objects.values(
        'categoria',
        'tipoviatico',
        'cantidadviajes',
        'cantidaddias',
        'zona',
        'justificacion',
        'filial__nombrefilial',
        'codcentrocosto__desccentrocosto',
        'codperiodo__descperiodo'
    ).filter(
        codperiodo=period,
        codcentrocosto=cost_center,
        habilitado=True).order_by('tipoviatico'))
    return create_excel_report(qs)


@login_required()
@permission_required(
    'ppto_viaticos.puede_registrar_egresos_viaticos', raise_exception=True
)
def check_out_travel(request):
    if request.is_ajax():
        if request.GET.get('method') == 'reserve':
            require_number = (
                f'{Transaccionesviaticos.objects.all().count()}'
                f'{dt.datetime.now().year}{dt.datetime.now().month}'
            )
            return HttpResponse(
                json.dumps({'require_number': require_number}),
                content_type='application/json'
            )
        elif request.GET.get('method') == 'require':
            id = request.GET.get('id', '')
            comments = Transaccionesviaticos.objects.values('comentario').filter(
                codmanejoviatico=id
            )
            settlement_number = (
                f'{Transaccionesviaticos.objects.all().count()}'
                f'{dt.datetime.now().year}{dt.datetime.now().month}'
                f'{Transaccionesviaticos.objects.all().count()}'
            )
            sql_statement = 'CONVERT(nvarchar(25), CAST(Comprometido as DECIMAL(23,2)))'
            requests = Transaccionesviaticos.objects.extra({
                'comprometido': sql_statement,
            }).values('numerosolicitud', 'comprometido', 'pk').filter(
                numeroliquidacion__isnull=True, codmanejoviatico=id
            )
            data = {
                'comments': list(comments),
                'settlement_number': settlement_number,
                'requests': list(requests),
            }
            return HttpResponse(json.dumps(data), content_type='application/json')

    if request.method == 'POST':
        if request.POST.get('method') == 'reserve':
            qs = get_object_or_404(Manejodeviaticos, pk=request.POST.get('id'))
            qs.reservado = float(qs.reservado) + float(request.POST.get('amount_reserve'))
            qs.usuariomodificacion = request.user
            qs.fechamodificacion = dt.datetime.today()
            qs.save()

            transaction = Transaccionesviaticos()
            transaction.comprometido = float(request.POST.get('amount_reserve'))
            transaction.codmanejoviatico = qs
            transaction.fechacreacion = request.POST.get('request_date')
            transaction.numerosolicitud = request.POST.get('correlative_reserve')
            transaction.usuariocreacion = request.user
            transaction.save()
            messages.success(request, 'Reserva realizada con ??xito!')

        elif request.POST.get('method') == 'require':
            qs = get_object_or_404(Manejodeviaticos, pk=request.POST.get('id'))
            if request.POST.get('request_number') == 'not_request_number':
                amount = float(request.POST.get('purchase_amount'))
                available = Manejodeviaticos.objects.extra(
                    {'disponible': 'Disponible'}
                ).values('disponible').get(pk=qs.pk)
                if amount > float(available.get('disponible')):
                    messages.warning(
                        request,
                        (
                            f'Requisici??n de viatico por valor {amount} '
                            f'mayor al disponible: {float(available.get("disponible"))}'
                        )
                    )
                    return redirect('check_out_travel')

                trans = Transaccionesviaticos()
                trans.codmanejoviatico = qs
                trans.requerido = request.POST.get('purchase_amount')
                trans.numeroliquidacion = request.POST.get('settlement_number')
                trans.usuariocreacion = request.user
                trans.fechacreacion = dt.datetime.today()
                trans.comentario = request.POST.get('comment')
                trans.save()

                executed = Transaccionesviaticos.objects.filter(
                    codmanejoviatico=trans.codmanejoviatico
                ).aggregate(Sum('requerido'))

                qs.comentario = request.POST.get('comment')
                qs.ejecutado = float(executed.get('requerido__sum'))
                qs.save()

            else:
                id_trans = request.POST.get('request_number')
                qs_trans = get_object_or_404(Transaccionesviaticos, pk=id_trans)
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
                            f'Requisici??n de viatico por valor {purchase_amount} '
                            f'mayor al disponible {amount_available} para '
                            f'n??mero de solicitud: {correlative_number}'
                        )
                    )
                    return redirect('check_out_travel')

                qs_trans.requerido = purchase_amount
                qs_trans.numeroliquidacion = request.POST.get('settlement_number')
                qs_trans.save()

                trans = Transaccionesviaticos()
                trans.coddetallexpresupuestoinversion = qs
                trans.requerido = purchase_amount
                trans.numeroliquidacion = request.POST.get('settlement_number')
                trans.usuariocreacion = request.user
                trans.fechacreacion = dt.datetime.today()
                trans.comentario = request.POST.get('comment')
                trans.save()

                qs.ejecutado = float(qs.ejecutado) + purchase_amount
                qs.reservado = qs.reservado - qs_trans.comprometido
                qs.usuariomodificacion = request.user
                qs.fechamodificacion = dt.datetime.today()
                qs.save()

            messages.success(request, 'Requisici??n de compra realizada con ??xito!')

    if request.GET.get('period') and request.GET.get('cost_center'):
        request.session['period'] = request.GET.get('period', '')
        request.session['cost_center'] = request.GET.get('cost_center', '')

    periods = Periodo.objects.filter(habilitado=True)
    cost_centers = Centroscosto.objects.filter(habilitado=True)
    ctx = {
        'periods': periods,
        'cost_centers': cost_centers,
    }

    if (
        request.session.get('period', None) and
        request.session.get('cost_center', None)
    ):
        cost_center = request.session['cost_center']
        period = request.session['period']
        page = request.GET.get('page', 1)
        q = request.GET.get('q', '')
        qs = Manejodeviaticos.objects.extra({
            'presupuestado': 'CAST(CAST(Presupuestado as DECIMAL(23,2)) as nvarchar(150))',
            'reservado': 'CAST(CAST(Reservado as DECIMAL(23,2)) as nvarchar(150))',
            'ejecutado': 'CAST(CAST(Ejecutado as DECIMAL(23,2)) as nvarchar(150))',
            'disponible': 'CAST(CAST(Disponible as DECIMAL(23,2)) as nvarchar(150))',
        }).values(
            'pk',
            'codmanejoviaticos',
            'codcentrocosto__desccentrocosto',
            'centropresupuestado__desccentrocosto',
            'presupuestado',
            'presupuestadocontraslado',
            'reservado',
            'ejecutado',
            'disponible',
            'periodo__descperiodo',
        ).filter(
            centropresupuestado=cost_center,
            periodo=period
        ).filter(
            Q(codcentrocosto__desccentrocosto__icontains=q)
        ).order_by('codcentrocosto__desccentrocosto')
        totales = qs.aggregate(
            presupuestado=Sum('presupuestado'),
            reservado=Sum('reservado'),
            ejecutado=Sum('ejecutado')
        )

        total_available = Manejodeviaticos.objects.extra({
            'disponible': 'SUM(Disponible)'
        }).values('disponible').filter(
            centropresupuestado=cost_center,
            periodo=period
        )

        ctx['qs'] = pagination(qs, page=page)
        ctx['total_executed'] = totales.get('ejecutado', '')
        ctx['total_reserved'] = totales.get('reservado', '')
        ctx['total_budget'] = totales.get('presupuestado', '')
        ctx['total_available'] = total_available[0].get('disponible', '')
    return render(request, 'check_out_travel/list.html', ctx)


@login_required()
def load_travel_distribution(request):
    if request.method == 'POST':
        file = load_excel_file(request.FILES['excel-file'])
        sheet = file.get('sheet')
        number_rows = file.get('number_rows')
        messages_exceptions = ''
        counter_u = 0
        counter_c = 0
        counter_e = 0
        for item in range(2, number_rows):
            try:
                qs_travel_budget = Detallexpresupuestoviaticos.objects.get(
                    pk=sheet[f'A{item}'].value
                )
                ceco_filial = Centroscosto.objects.get(
                    agencia=qs_travel_budget.filial.pk
                )
                qs = Manejodeviaticos.objects.filter(
                    periodo=qs_travel_budget.codperiodo.pk,
                    centropresupuestado=qs_travel_budget.codcentrocosto.pk,
                    codcentrocosto=ceco_filial.pk,
                    categoria=sheet[f'E{item}'].value
                ).first()
                amount = sheet[f'H{item}'].value
                if qs:

                    _upd = Manejodeviaticos.objects.get(pk=qs.pk)
                    _upd.presupuestado = amount
                    _upd.presupuestadocontraslado = amount
                    _upd.reservado = 0
                    _upd.ejecutado = 0
                    _upd.periodo = qs_travel_budget.codperiodo
                    _upd.centropresupuestado = qs_travel_budget.codcentrocosto
                    _upd.codcentrocosto = ceco_filial
                    _upd.categoria = sheet[f'E{item}'].value
                    _upd.fechacreacion = dt.datetime.today()
                    _upd.usuariocreacion = request.user
                    _upd.save()
                    counter_u = counter_u + 1
                else:
                    _new = Manejodeviaticos()
                    _new.presupuestado = amount
                    _new.presupuestadocontraslado = amount
                    _new.reservado = 0
                    _new.ejecutado = 0
                    _new.periodo = qs_travel_budget.codperiodo
                    _new.centropresupuestado = qs_travel_budget.codcentrocosto
                    _new.codcentrocosto = ceco_filial
                    _new.categoria = sheet[f'E{item}'].value
                    _new.fechacreacion = dt.datetime.today()
                    _new.usuariocreacion = request.user
                    _new.save()
                    counter_c = counter_c + 1
            except Centroscosto.DoesNotExist:
                counter_e = counter_e + 1
                messages_exceptions = (
                    f'{messages_exceptions} </br>'
                    f'Filial: {qs_travel_budget.filial.nombrefilial} '
                    f'No existe como Centro de Costos. Linea # {item}'
                )
            except Detallexpresupuestoviaticos.DoesNotExist:
                counter_e = counter_e + 1
                messages_exceptions = (
                    f'{messages_exceptions} </br>'
                    f'Identificador: {sheet[f"A{item}"].value} no coindice '
                    f'Linea # {item}'
                )
            except Exception as e:
                counter_e = counter_e + 1
                messages_exceptions = (
                    f'{messages_exceptions} </br>'
                    f'{e.__str__()}'
                    f'Linea # {item}'
                )

        messages.warning(
            request,
            (
                f'Total lineas con errores: {counter_e} </br>'
                f'{messages_exceptions}'
            ),
            extra_tags='safe'
        )
        messages.success(
            request,
            f'Creadas: {counter_c} </br> Actualizadas: {counter_u}',
            extra_tags='safe'
        )

    if request.method == 'GET':
        if request.GET.get('method') == 'filter':
            request.session['period'] = request.GET.get('period')

        elif request.GET.get('method') == 'download-file':
            request.session['period'] = request.GET.get('period')
            qs = Detallexpresupuestoviaticos.objects.filter(
                tipoviatico=1,
                habilitado=True,
                codperiodo=request.session['period']
            ).order_by(
                'codcentrocosto__desccentrocosto',
                'filial__nombrefilial'
            )
            return generate_excel_file_format_distribution(qs)

    periods = Periodo.objects.filter(habilitado=True)
    ctx = {
        'periods': periods
    }

    if request.session.get('period'):
        page = request.GET.get('page', 1)
        period = request.session.get('period')
        qs = Manejodeviaticos.objects.extra({
            'presupuestado': 'CAST(CAST(Presupuestado as DECIMAL(23,2)) as nvarchar(150))',
            'reservado': 'CAST(CAST(Reservado as DECIMAL(23,2)) as nvarchar(150))',
            'ejecutado': 'CAST(CAST(Ejecutado as DECIMAL(23,2)) as nvarchar(150))',
            'disponible': 'CAST(CAST(Disponible as DECIMAL(23,2)) as nvarchar(150))',
        }).values(
            'pk',
            'codmanejoviaticos',
            'codcentrocosto__desccentrocosto',
            'centropresupuestado__desccentrocosto',
            'presupuestado',
            'presupuestadocontraslado',
            'reservado',
            'ejecutado',
            'disponible',
            'periodo__descperiodo',
        ).filter(
            periodo=period
        ).order_by('centropresupuestado__desccentrocosto')

        result = pagination(qs, page, page_size=200)
        ctx['qs'] = result

    return render(request, 'load_travel_distribution/list.html', ctx)
