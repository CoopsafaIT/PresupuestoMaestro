import json
from decimal import Decimal as dc
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import PermissionDenied, ValidationError

from utils.sql import execute_sql_query
from utils.pagination import pagination
from .reports import (
    generate_subsidiary_goal_excel_file,
    load_excel_file,
    generate_subsidiary_goal_execute_excel_file,
    generate_report_by_subsidiary
)
from apps.main.models import ResponsablesPorCentrosCostos, Centroscosto, Periodo
from .models import (
    GlobalGoalPeriod, GlobalGoalDetail, Goal,
    SubsidiaryGoalDetail
)
from .forms import (
    GoalsPeriodForm, GoalsForm, GlobalGoalDetailForm
)
from .request_get import QueryGetParms
from utils.constants import MONTH_CHOICES, MONTHS_LIST


@login_required()
@permission_required('goals.puede_ver_menu_de_metas', raise_exception=True)
def goals_dashboard(request):

    def _get_report_data():
        period = request.GET.get('period')
        month = request.GET.get('month', 12)
        ceco = _set_ceco(request.GET.getlist('ceco[]'))

        QUERY_SP = f"EXEC [dbo].[spMetasEjecucionPorAgenciaListar] @CodPeriodo={period}, @Mes={month}, @CodAgencia='{ceco}'" # NOQA
        return execute_sql_query(QUERY_SP)

    def _set_ceco(request_ceco):
        if len(request_ceco) > 1:
            return ','.join(request_ceco)
        return request_ceco[0]

    def _define_thead_labels():
        month = int(request.GET.get('month'))
        months = []
        for index, month_letters in enumerate(MONTHS_LIST, start=1):
            if(index <= month):
                months.append(month_letters)
        return months

    if (
        request.user.has_perm('goals.puede_ver_metas_todos_centros_costos') is False and
        request.user.has_perm('goals.puede_ver_metas_centros_costos_asignadas') is False
    ):
        raise PermissionDenied
    if request.is_ajax():
        result = _get_report_data()
        if result.get('status') != 'ok':
            return HttpResponse(
                json.dumps({'message': result.get('data')}, cls=DjangoJSONEncoder),
                status=500
            )
        else:
            data = result.get('data')
            months_labels = _define_thead_labels()
            return HttpResponse(
                json.dumps({'data': data, 'months_labels': months_labels}, cls=DjangoJSONEncoder) # NOQA
            )

    elif request.method == 'GET':
        if request.GET.get('period') and request.GET.getlist('ceco[]'):
            result = _get_report_data()
            if result.get('status') != 'ok':
                messages.error(request, 'No se pudo completar acción')
            else:
                data = result.get('data')
                months_labels = _define_thead_labels()
                return generate_report_by_subsidiary(data, months_labels)

    periods = Periodo.objects.filter(habilitado=True)
    if request.user.has_perm('goals.puede_ver_metas_todos_centros_costos'):
        cecos = Centroscosto.objects.filter(habilitado=True).exclude(code_zone='0').exclude(code_zone__isnull=True) # NOQA
    else:
        qs_res_cecos = ResponsablesPorCentrosCostos.objects.filter(
            CodUser=request.user.id, Estado=True
        ).values_list('CodCentroCosto__pk', flat=True)
        cecos = Centroscosto.objects.filter(
            pk__in=qs_res_cecos, habilitado=True
        ).exclude(code_zone='0').exclude(code_zone__isnull=True)

    ctx = {
        'cecos': cecos,
        'periods': periods,
        'months': MONTH_CHOICES
    }
    return render(request, 'goals/dashboard.html', ctx)


@login_required()
@permission_required('goals.puede_listar_metas', raise_exception=True)
def goals(request):
    form = GoalsForm()
    if request.method == 'POST':
        if not request.user.has_perm('goals.puede_ingresar_metas'):
            raise PermissionDenied
        try:
            form = GoalsForm(request.POST)
            if not form.is_valid():
                messages.warning(
                    request, f'Formulario no válido: {form.errors.as_text()}'
                )
            else:
                _new = form.save()
                _new.created_by = request.user
                _new.updated_by = request.user
                _new.save()
                messages.success(request, 'Meta creada con éxito!')
        except ValidationError as e:
            messages.warning(
                request,
                f'Error de validación: {e.__str__()}'
            )
        except Exception as e:
            messages.error(
                request,
                f'Error al ingresar meta. {e.__str__()}'
            )
    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')
    qs = Goal.objects.filter(
        Q(description__icontains=q) | Q(type__icontains=q) |
        Q(definition__icontains=q) | Q(execution__icontains=q)
    ).order_by('description')
    result = pagination(qs, page)

    ctx = {
        'result': result,
        'form': form,
    }
    return render(request, 'goals_definition/goals.html', ctx)


@login_required()
@permission_required('goals.puede_editar_metas', raise_exception=True)
def goal_edit(request, id):
    qs = get_object_or_404(Goal, pk=id)
    form = GoalsForm(instance=qs)
    if request.method == 'POST':
        if request.POST.get('method') == 'edit':
            form = GoalsForm(request.POST, instance=qs)
            if not form.is_valid():
                messages.warning(
                    request,
                    f'Formulario no válido: {form.errors.as_text()}'
                )
            else:
                if request.POST.get('is_active') == 'True':
                    Goal.objects.filter(
                        id=qs.id
                    ).update(is_active=False)
                _new = form.save()
                _new.updated_by = request.user
                _new.save()
                messages.success(request, 'Meta editada con éxito!')
                return redirect('goals')
    ctx = {
        'form': form
    }
    return render(request, 'goals_definition/goals_edit.html', ctx)


@login_required()
@permission_required(
    'goals.puede_listar_definicion_de_periodo_de_meta', raise_exception=True
)
def global_goals_period(request):
    form = GoalsPeriodForm()
    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')
    qs = GlobalGoalPeriod.objects.filter(
        Q(description__icontains=q) |
        Q(period_id__descperiodo__icontains=q)
    ).order_by('period_id')
    result = pagination(qs, page)

    ctx = {
        'result': result,
        'form': form
    }
    return render(request, 'goals_period/goals_period_list.html', ctx)


@login_required()
@permission_required('goals.puede_editar_periodo_de_meta', raise_exception=True)
def goals_period_edit(request, id):
    qs = get_object_or_404(GlobalGoalPeriod, pk=id)
    form = GoalsPeriodForm(instance=qs)

    if request.method == 'POST':
        if request.POST.get('method') == 'edit':
            form = GoalsPeriodForm(request.POST, instance=qs)
            if not form.is_valid():
                messages.warning(
                    request,
                    f'Formulario no válido: {form.errors.as_text()}'
                )
            else:
                if request.POST.get('is_active') == 'True':
                    GlobalGoalPeriod.objects.filter(
                        period_id=qs.period_id
                    ).update(is_active=False)
                _new = form.save()
                _new.updated_by = request.user
                _new.save()
                messages.success(request, 'Meta editada con éxito!')
                return redirect('global_goals_period')
    ctx = {
        'form': form
    }
    return render(request, 'goals_definition/goals_edit.html', ctx)


@login_required()
def goals_global_definition(request, id_global_goal_period):
    if (
        not request.user.has_perm('goals.puede_ver_definicion_de_meta_asignada') and
        not request.user.has_perm('goals.puede_ver_definicion_de_meta')
    ):
        raise PermissionDenied
    qs_global_goal_period = get_object_or_404(GlobalGoalPeriod, pk=id_global_goal_period)
    qs_goals = Goal.objects.all().order_by('description')
    qs_global_goal_detail = GlobalGoalDetail.objects.filter(
        id_global_goal_period=qs_global_goal_period.pk
    )

    def _validate(data):
        annual_amount = float(data.get('annual_amount'))
        amount_december = float(data.get('amount_december'))
        if annual_amount == amount_december:
            return {
                'status': 'ok', 'message': ''
            }
        else:
            return {
                'status': 'error',
                'message': 'Monto distribución mensaual no es igual a monto anual'
            }

    if request.is_ajax():
        if request.method == 'POST':
            if not request.user.has_perm('goals.puede_ver_detalle_mensual_de_metas_globales'): # NOQA
                raise PermissionDenied
            data = json.loads(request.POST.get('data'))
            goal_id = data.pop('goal_id')
            qs = Goal.objects.filter(pk=goal_id).first()

            result = _validate(data)
            if result.get('status') == 'ok':
                GlobalGoalDetail.objects.filter(
                    id_goal=goal_id, id_global_goal_period=qs_global_goal_period.pk
                ).update(**data)
                return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder))
            else:
                return HttpResponse(
                    json.dumps({'message': result.get('message')}, cls=DjangoJSONEncoder),
                    status=400
                )

        elif request.method == 'GET':
            goal_id = request.GET.get('goalId')
            if request.GET.get('method') == 'get-goal-detail':
                if not request.user.has_perm('goals.puede_registrar_metas_globales'):
                    raise PermissionDenied
                qs = Goal.objects.filter(pk=goal_id).first()
                if qs.definition == "A":
                    query = f'EXEC {qs.query}'
                    query = query.replace(
                        '__periodId__', f'{qs_global_goal_period.period_id.pk}'
                    )
                    result = execute_sql_query(query)
                    if result.get('status') != 'ok':
                        ctx = {
                            'message': 'No se pudo obtener el monto de la meta'
                        }
                        return HttpResponse(
                            json.dumps(ctx, cls=DjangoJSONEncoder), status=500
                        )
                    data = result.get('data')
                    data = data[0]
                    goal_monthly_definition = {
                        key.lower(): value for key, value in data.items()
                    }
                else:
                    goal_monthly_definition = {
                        'total': 0,
                        'ene': 0, 'feb': 0, 'mar': 0, 'abr': 0,
                        'may': 0, 'jun': 0, 'jul': 0, 'ago': 0,
                        'sep': 0, 'oct': 0, 'nov': 0, 'dic': 0,
                    }
                ctx = {
                    'goal_monthly_definition': goal_monthly_definition,
                    'definition': qs.definition
                }
                return HttpResponse(json.dumps(ctx, cls=DjangoJSONEncoder))
            elif request.GET.get('method') == 'get-global-goal-detail':
                if not request.user.has_perm('goals.puede_ver_detalle_mensual_de_metas_globales'): # NOQA
                    raise PermissionDenied
                qs_goal = Goal.objects.values(
                    'id', 'description', 'definition'
                ).get(pk=goal_id)
                qs_global_goal = GlobalGoalDetail.objects.values(
                    'amount_january', 'amount_february', 'amount_march',
                    'amount_april', 'amount_may', 'amount_june',
                    'amount_july', 'amount_august', 'amount_september',
                    'amount_october', 'amount_november', 'amount_december',
                    'annual_amount', 'ponderation'
                ).filter(
                    id_goal=qs_goal.get('id'),
                    id_global_goal_period=qs_global_goal_period.pk
                ).first()
                ctx = {
                    'qs_goal': qs_goal,
                    'qs_global_goal': qs_global_goal
                }
                return HttpResponse(json.dumps(ctx, cls=DjangoJSONEncoder))

    elif request.method == 'POST':
        if not request.user.has_perm('goals.puede_registrar_metas_globales'):
            raise PermissionDenied
        post = request.POST.copy()
        post['annual_amount'] = post.get('annual_amount').replace(',', '')

        form = GlobalGoalDetailForm(post)
        if not form.is_valid():
            messages.warning(
                request, f'formulario no valido: {form.errors.as_text()}'
            )
        else:
            _new = form.save()
            _new.created_by = request.user
            _new.updated_by = request.user
            _new.save()

            definition = _new.id_goal.definition
            if definition == 'A':
                query = f'EXEC {_new.id_goal.query}'
                query = query.replace(
                    '__periodId__', f'{qs_global_goal_period.period_id.pk}'
                )
                result = execute_sql_query(query)
                if result.get('status') != 'ok':
                    messages.warning(
                        request, 'No se pudo obtener montos mensuales de Metas'
                    )
                else:
                    data = result.get('data')
                    data = data[0]
                    _new.amount_january = data.get('Ene')
                    _new.amount_february = data.get('Feb')
                    _new.amount_march = data.get('Mar')
                    _new.amount_april = data.get('Abr')
                    _new.amount_may = data.get('May')
                    _new.amount_june = data.get('Jun')
                    _new.amount_july = data.get('Jul')
                    _new.amount_august = data.get('Ago')
                    _new.amount_september = data.get('Sep')
                    _new.amount_october = data.get('Oct')
                    _new.amount_november = data.get('Nov')
                    _new.amount_december = data.get('Dic')
                    _new.annual_amount = data.get('Total')
                    _new.save()

            messages.success(request, 'Meta agregada con éxito')

    filters = {}
    if not request.user.has_perm('goals.puede_ver_definicion_de_meta'):
        filters = {'id_goal__user_assigned__id': request.user.id}

    qs_global_goal_detail = GlobalGoalDetail.objects.filter(
        id_global_goal_period=qs_global_goal_period.pk
    ).filter(**filters)

    exclude = qs_global_goal_detail.values_list('id_goal', flat=True)
    qs_goals = Goal.objects.exclude(pk__in=exclude).order_by('description')
    qs_sum = qs_global_goal_detail.extra({
        'sum_amount': 'SUM(MontoAnual)',
        'sum_ponderation': 'SUM(Ponderacion)'
    }).values('sum_amount', 'sum_ponderation')
    qs_sum = qs_sum[0]
    ctx = {
        'qs_global_goal_period': qs_global_goal_period,
        'qs_goals': qs_goals,
        'sum_amount': qs_sum.get('sum_amount'),
        'sum_ponderation': qs_sum.get('sum_ponderation'),
        'qs_global_goal_detail': qs_global_goal_detail
    }

    return render(request, 'goals_definition/goals_global_definition.html', ctx)


@login_required()
@permission_required('goals.puede_ver_definicion_de_meta_por_filial', raise_exception=True)
def subsidiary_goals_definition(request, id_global_goal_definition):
    qs_global_detail = get_object_or_404(GlobalGoalDetail, pk=id_global_goal_definition) # NOQA
    zones_requested = request.GET.getlist('code_zone')
    query_parms = QueryGetParms(request.GET)
    qs_zone = []
    query = (
        "SELECT DISTINCT CodZona as code_zone, Zona AS zone FROM "
        "[CentrosCosto] WHERE CodZona is not null"
    )

    def _get_qs_subsidiary_list():
        return SubsidiaryGoalDetail.objects.filter(
            id_global_goal_detail=id_global_goal_definition
        ).filter(**query_parms.get_query_filters()).order_by(
            'id_cost_center__code_zone', 'id_cost_center__desccentrocosto'
        )

    def _get_sum_amount_goal_definition(filters={}, exclude={}):
        return SubsidiaryGoalDetail.objects.extra({
            'sum_total': 'SUM(MontoAnualFilial)',
            'sum_ene': 'SUM(MontoEne)', 'sum_feb': 'SUM(MontoFeb)',
            'sum_mar': 'SUM(MontoMar)', 'sum_abr': 'SUM(MontoAbr)',
            'sum_may': 'SUM(MontoMay)', 'sum_jul': 'SUM(MontoJun)',
            'sum_jun': 'SUM(MontoJul)', 'sum_ago': 'SUM(MontoAgo)',
            'sum_sep': 'SUM(MontoSep)', 'sum_oct': 'SUM(MontoOct)',
            'sum_nov': 'SUM(MontoNov)', 'sum_dic': 'SUM(MontoDic)',
        }).filter(
            id_global_goal_detail=id_global_goal_definition
        ).filter(**filters).exclude(**exclude).values(
            'sum_total', 'sum_ene', 'sum_feb', 'sum_mar',
            'sum_abr', 'sum_may', 'sum_jul',
            'sum_jun', 'sum_ago', 'sum_sep',
            'sum_oct', 'sum_nov', 'sum_dic'
        )

    def _calculate_new_amounts(id, data):
        qs_sum = _get_sum_amount_goal_definition(
            filters=query_parms.get_query_filters(), exclude={'id': id}
        )
        qs_sum = qs_sum[0]
        new_amounts = {
            'total': (qs_sum.get('sum_total') + dc(data.get('annual_amount_subsidiary'))),
            'amount_january': (qs_sum.get('sum_ene') + dc(data.get('amount_january'))),
            'amount_february': (qs_sum.get('sum_feb') + dc(data.get('amount_february'))),
            'amount_march': (qs_sum.get('sum_mar') + dc(data.get('amount_march'))),
            'amount_april': (qs_sum.get('sum_abr') + dc(data.get('amount_april'))),
            'amount_may': (qs_sum.get('sum_may') + dc(data.get('amount_may'))),
            'amount_june': (qs_sum.get('sum_jun') + dc(data.get('amount_june'))),
            'amount_july': (qs_sum.get('sum_jul') + dc(data.get('amount_july'))),
            'amount_august': (qs_sum.get('sum_ago') + dc(data.get('amount_august'))),
            'amount_september': (qs_sum.get('sum_sep') + dc(data.get('amount_september'))),
            'amount_october': (qs_sum.get('sum_oct') + dc(data.get('amount_october'))),
            'amount_november': (qs_sum.get('sum_nov') + dc(data.get('amount_november'))),
            'amount_december': (qs_sum.get('sum_dic') + dc(data.get('amount_december')))
        }

        if qs_global_detail.annual_amount < new_amounts.get('total'):
            return {
                'status': 'err',
                'msg': f'Con el nuevo monto anual {data.get("annual_amount_subsidiary")} excede el Monto Total Global' # NOQA
            }
        if qs_global_detail.amount_january < new_amounts.get('amount_january'):
            return {
                'status': 'err',
                'msg': f'Con el nuevo monto en enero {data.get("amount_january")} excede el Monto Global en Enero' # NOQA
            }
        if qs_global_detail.amount_february < new_amounts.get('amount_february'):
            return {
                'status': 'err',
                'msg': f'Con el nuevo monto en febrero {data.get("amount_february")} se excede el Monto Global de febrero' # NOQA
            }
        if qs_global_detail.amount_march < new_amounts.get('amount_march'):
            return {
                'status': 'err',
                'msg': f'Con el nuevo monto en marzo {data.get("amount_march")} se excede el Monto Global de marzo' # NOQA
            }
        if qs_global_detail.amount_april < new_amounts.get('amount_april'):
            return {
                'status': 'err',
                'msg': f'Con el nuevo monto en abril {data.get("amount_april")} se excede el Monto Global de abril' # NOQA
            }
        if qs_global_detail.amount_may < new_amounts.get('amount_may'):
            return {
                'status': 'err',
                'msg': f'Con el nuevo monto en mayo {data.get("amount_may")} se excede el Monto Global de mayo' # NOQA
            }
        if qs_global_detail.amount_june < new_amounts.get('amount_june'):
            return {
                'status': 'err',
                'msg': f'Con el nuevo monto en junio {data.get("amount_june")} se excede el Monto Global de junio' # NOQA
            }
        if qs_global_detail.amount_july < new_amounts.get('amount_july'):
            return {
                'status': 'err',
                'msg': f'Con el nuevo monto en julio {data.get("amount_july")} se excede el Monto Global de julio' # NOQA
            }
        if qs_global_detail.amount_august < new_amounts.get('amount_august'):
            return {
                'status': 'err',
                'msg': f'Con el nuevo monto en agosto {data.get("amount_august")} se excede el Monto Global de agosto' # NOQA
            }
        if qs_global_detail.amount_september < new_amounts.get('amount_september'):
            return {
                'status': 'err',
                'msg': f'Con el nuevo monto en septiembre {data.get("amount_september")} se excede el Monto Global de septiembre' # NOQA
            }
        if qs_global_detail.amount_october < new_amounts.get('amount_october'):
            return {
                'status': 'err',
                'msg': f'Con el nuevo monto en octubre {data.get("amount_october")} se excede el Monto Global de octubre' # NOQA
            }
        if qs_global_detail.amount_november < new_amounts.get('amount_november'):
            return {
                'status': 'err',
                'msg': f'Con el nuevo monto en noviembre {data.get("amount_november")} se excede el Monto Global de noviembre' # NOQA
            }
        if qs_global_detail.amount_december < new_amounts.get('amount_december'):
            return {
                'status': 'err',
                'msg': f'Con el nuevo monto en diciembre {data.get("amount_december")} se excede el Monto Global de diciembre' # NOQA
            }

        return {'status': 'ok', 'msg': ''}

    def _validate_subsidiary_data(id, dict_data):
        qs_subsidiary = SubsidiaryGoalDetail.objects.filter(pk=id).first()
        if not qs_subsidiary:
            return {'status': 'err', 'msg': 'Meta de Filial no encontrada'}
        total = dc(dict_data.pop('annual_amount_subsidiary'))
        values = [dc(month) for month in list(dict_data.values())]
        sum_months = sum(values)
        if not total == round(sum_months):
            return {
                'status': 'err',
                'msg': f'Suma de meses {sum_months} diferente a total: {total}'
            }
        return {'status': 'ok', 'msg': ''}

    def _validate_subsidiary_execution(id):
        qs_subsidiary = SubsidiaryGoalDetail.objects.filter(pk=id).first()
        if not qs_subsidiary:
            return {'status': 'err', 'msg': 'Meta de Filial no encontrada'}
        return {'status': 'ok', 'msg': ''}

    if request.is_ajax():
        if request.method == 'POST':
            data = json.loads(request.POST.get('data'))
            id = data.pop('id')
            result = _validate_subsidiary_data(id=id, dict_data=data.copy())
            if result.get('status') != 'ok':
                return HttpResponse(
                    json.dumps({'message': result.get('msg')}, cls=DjangoJSONEncoder),
                    status=400
                )
            result = _calculate_new_amounts(id, data)
            if result.get('status') != 'ok':
                return HttpResponse(
                    json.dumps({'message': result.get('msg')}, cls=DjangoJSONEncoder),
                    status=400
                )

            SubsidiaryGoalDetail.objects.filter(pk=id).update(**data)
            return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder))

    elif request.method == 'GET':
        if request.GET.get('method') == 'excel':
            if not request.user.has_perm('goals.puede_ingresar_definiciones_manuales'):
                raise PermissionDenied
            qs_data = _get_qs_subsidiary_list()
            return generate_subsidiary_goal_excel_file(qs_data, qs_global_detail)

        if request.GET.get('method') == 'excel-execution':
            if not request.user.has_perm('goals.puede_ingresar_ejecuciones_manuales'):
                raise PermissionDenied
            qs_data = _get_qs_subsidiary_list()
            return generate_subsidiary_goal_execute_excel_file(qs_data, qs_global_detail) # NOQA

    elif request.method == 'POST':
        if request.POST.get('method') == 'load-excel':
            if not request.user.has_perm('goals.puede_ingresar_definiciones_manuales'):
                raise PermissionDenied
            result = load_excel_file(request.FILES['excel-file'])
            sheet = result.get('sheet')
            number_rows = result.get('number_rows')
            counter = 2
            for item in range(1, number_rows):
                id = sheet[f'A{counter}'].value
                ponderation = sheet[f'Q{counter}'].value
                data = {
                    'annual_amount_subsidiary':  sheet[f'D{counter}'].value,
                    'amount_january': sheet[f'E{counter}'].value,
                    'amount_february': sheet[f'F{counter}'].value,
                    'amount_march': sheet[f'G{counter}'].value,
                    'amount_april': sheet[f'H{counter}'].value,
                    'amount_may': sheet[f'I{counter}'].value,
                    'amount_june': sheet[f'J{counter}'].value,
                    'amount_july': sheet[f'K{counter}'].value,
                    'amount_august': sheet[f'L{counter}'].value,
                    'amount_september': sheet[f'M{counter}'].value,
                    'amount_october': sheet[f'N{counter}'].value,
                    'amount_november': sheet[f'O{counter}'].value,
                    'amount_december': sheet[f'P{counter}'].value
                }
                result_validate = _validate_subsidiary_data(id=id, dict_data=data.copy())
                result_calculate = _calculate_new_amounts(id, data)
                if result_validate.get('status') != 'ok':
                    messages.error(
                        request, f'Error. Identificador: {id} {result_validate.get("msg")}'
                    )
                elif result_calculate.get('status') != 'ok':
                    messages.error(
                        request, f'Error. Identificador: {id} {result_validate.get("msg")}'
                    )
                else:
                    SubsidiaryGoalDetail.objects.filter(pk=id).update(
                        ponderation=ponderation, **data
                    )
                counter = counter + 1

        if request.POST.get('method') == 'load-excel-execution':
            if not request.user.has_perm('goals.puede_ingresar_ejecuciones_manuales'):
                raise PermissionDenied
            result = load_excel_file(request.FILES['excel-file'])
            sheet = result.get('sheet')
            number_rows = result.get('number_rows')
            counter = 2
            for item in range(1, number_rows):
                id = sheet[f'A{counter}'].value
                try:
                    data = {
                        'amount_exec_january': dc(sheet[f'D{counter}'].value),
                        'amount_exec_february': dc(sheet[f'E{counter}'].value),
                        'amount_exec_march': dc(sheet[f'F{counter}'].value),
                        'amount_exec_april': dc(sheet[f'G{counter}'].value),
                        'amount_exec_may': dc(sheet[f'H{counter}'].value),
                        'amount_exec_june': dc(sheet[f'I{counter}'].value),
                        'amount_exec_july': dc(sheet[f'J{counter}'].value),
                        'amount_exec_august': dc(sheet[f'K{counter}'].value),
                        'amount_exec_september': dc(sheet[f'L{counter}'].value),
                        'amount_exec_october': dc(sheet[f'M{counter}'].value),
                        'amount_exec_november': dc(sheet[f'N{counter}'].value),
                        'amount_exec_december': dc(sheet[f'O{counter}'].value)
                    }
                except Exception as e:
                    messages.error(
                        request,
                        f'La linea {counter} con identificador {id} no pudo ser ingresado {e}'# NOQA
                    )
                else:
                    result_validate_execution = _validate_subsidiary_execution(id=id)
                    if result_validate_execution.get('status') != 'ok':
                        messages.error(
                            request,
                            f'Error. Identificador: {id} {result_validate_execution.get("msg")}'# NOQA
                        )
                    else:
                        SubsidiaryGoalDetail.objects.filter(pk=id).update(**data)
                finally:
                    counter = counter + 1

    query_result = execute_sql_query(query)
    if query_result.get('status') == 'ok':
        qs_zone = query_result.get('data')

    qs_subsidiary_list = _get_qs_subsidiary_list()
    qs_sum = _get_sum_amount_goal_definition(filters=query_parms.get_query_filters())
    qs_goal = qs_subsidiary_list.first().id_goal.execution
    ctx = {
        'qs_global_detail': qs_global_detail,
        'qs_subsidiary_list': qs_subsidiary_list,
        'qs_zone': qs_zone,
        'qs_sum': qs_sum[0],
        'qs_goal': qs_goal,
        'zones_requested': zones_requested
    }
    return render(request, 'goals_definition/subsidiary_goals_definition.html', ctx)


@login_required()
@permission_required('goals.puede_ver_detalle_filial', raise_exception=True)
def subsidiary_goals_detail(request, id_cost_center, id_global_goal_period):
    qs = list(SubsidiaryGoalDetail.objects.filter(
        id_cost_center=id_cost_center, id_global_goal_period=id_global_goal_period
    ).values(
        'id_goal__description', 'annual_amount_subsidiary', 'ponderation',
        'amount_january', 'amount_february', 'amount_march',
        'amount_april', 'amount_may', 'amount_june',
        'amount_july', 'amount_august', 'amount_september',
        'amount_october', 'amount_november', 'amount_december'
    ).order_by('id_goal__description'))

    qs_sum = list(SubsidiaryGoalDetail.objects.extra({
        'sum_total': 'SUM(MontoAnualFilial)',
        'sum_ene': 'SUM(MontoEne)', 'sum_feb': 'SUM(MontoFeb)',
        'sum_mar': 'SUM(MontoMar)', 'sum_abr': 'SUM(MontoAbr)',
        'sum_may': 'SUM(MontoMay)', 'sum_jul': 'SUM(MontoJun)',
        'sum_jun': 'SUM(MontoJul)', 'sum_ago': 'SUM(MontoAgo)',
        'sum_sep': 'SUM(MontoSep)', 'sum_oct': 'SUM(MontoOct)',
        'sum_nov': 'SUM(MontoNov)', 'sum_dic': 'SUM(MontoDic)',
        'sum_ponderation': 'SUM(Ponderacion)'
    }).filter(
        id_cost_center=id_cost_center, id_global_goal_period=id_global_goal_period
    ).values(
        'sum_total', 'sum_ene', 'sum_feb', 'sum_mar',
        'sum_abr', 'sum_may', 'sum_jul',
        'sum_jun', 'sum_ago', 'sum_sep',
        'sum_oct', 'sum_nov', 'sum_dic', 'sum_ponderation'
    ))

    ctx = {
        'qs_sum': qs_sum[0], 'qs': qs
    }

    return HttpResponse(json.dumps(ctx, cls=DjangoJSONEncoder))
