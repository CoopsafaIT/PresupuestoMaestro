import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder


# from decimal import Decimal as dc

from utils.pagination import pagination
from .models import (
    GlobalGoalPeriod, GlobalGoalDetail, Goal
)
from .forms import (
    GoalsForm, GoalsGlobalForm, GlobalGoalDetailForm
)


@login_required()
def goals_dashboard(request):
    return render(request, 'goals/dashboard.html')


@login_required()
def goals_for_period(request):
    form = GoalsForm()
    if request.method == 'POST':
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
def goals_period(request, id):
    qs = get_object_or_404(GlobalGoalPeriod, pk=id)
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
                    GlobalGoalPeriod.objects.filter(
                        period_id=qs.period_id
                    ).update(is_active=False)
                _new = form.save()
                _new.updated_by = request.user
                _new.save()
                messages.success(request, 'Meta editada con éxito!')
                return redirect('goals_for_period')
    ctx = {
        'form': form
    }
    return render(request, 'goals_period/goals_period_edit.html', ctx)


@login_required()
def goals_global_definition(request, id_global_goal_period):
    qs_global_goal_period = get_object_or_404(GlobalGoalPeriod, pk=id_global_goal_period)
    qs_goals = Goal.objects.all().order_by('description')
    qs_global_goal_detail = GlobalGoalDetail.objects.filter(
        id_global_goal_period=qs_global_goal_period.pk
    )

    def _validate():
        data = json.loads(request.POST.get('data'))
        annual_amount = float(data.get('annual_amount'))
        amount_january = float(data.get('amount_january'))
        amount_february = float(data.get('amount_february'))
        amount_march = float(data.get('amount_march'))
        amount_april = float(data.get('amount_april'))
        amount_may = float(data.get('amount_may'))
        amount_june = float(data.get('amount_june'))
        amount_july = float(data.get('amount_july'))
        amount_august = float(data.get('amount_august'))
        amount_september = float(data.get('amount_september'))
        amount_october = float(data.get('amount_october'))
        amount_november = float(data.get('amount_november'))
        amount_december = float(data.get('amount_december'))
        sum = (
            amount_january + amount_february + amount_march + amount_april + amount_may +
            amount_june + amount_july + amount_august + amount_september + amount_october +
            amount_november + amount_december
        )
        if annual_amount == sum:
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
            data = json.loads(request.POST.get('data'))
            goal_id = data.pop('goal_id')

            result = _validate()

            if result.get('status') == 'ok':
                GlobalGoalDetail.objects.filter(
                    id_goal=goal_id, id_global_goal_period=qs_global_goal_period.pk
                ).update(**data)
                return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder))
            else:
                return HttpResponse(json.dumps(
                    {'message': result.get('message')},
                    cls=DjangoJSONEncoder), status=400
                )
            # Validar que suma de meses sea igual a monto anual

        elif request.method == 'GET':
            goal_id = request.GET.get('goalId')
            if request.GET.get('method') == 'get-goal-detail':
                qs = Goal.objects.filter(pk=goal_id).first()
                if qs.definition == "A":
                    goal_monthly_definition = {
                        'annual_amount': 10000,
                        'ene': 10000 / 12,
                        'feb': 10000 / 12,
                        'mar': 10000 / 12,
                        'abr': 10000 / 12,
                        'may': 10000 / 12,
                        'jun': 10000 / 12,
                        'jul': 10000 / 12,
                        'ago': 10000 / 12,
                        'sep': 10000 / 12,
                        'oct': 10000 / 12,
                        'nov': 10000 / 12,
                        'dic': 10000 / 12,
                    }
                else:
                    goal_monthly_definition = {
                        'annual_amount': 0,
                        'ene': 0,
                        'feb': 0,
                        'mar': 0,
                        'abr': 0,
                        'may': 0,
                        'jun': 0,
                        'jul': 0,
                        'ago': 0,
                        'sep': 0,
                        'oct': 0,
                        'nov': 0,
                        'dic': 0,
                    }
                ctx = {
                    'goal_monthly_definition': goal_monthly_definition,
                    'definition': qs.definition
                }
                return HttpResponse(json.dumps(ctx, cls=DjangoJSONEncoder))
            elif request.GET.get('method') == 'get-global-goal-detail':
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
        form = GlobalGoalDetailForm(request.POST)
        if not form.is_valid():
            messages.warning(
                request, f'formulario no valido: {form.errors.as_text()}'
            )
        else:
            _new = form.save()
            _new.created_by = request.user
            _new.updated_by = request.user
            _new.save()
            messages.success(request, 'Meta agregada con éxito')

    qs_goals = Goal.objects.all().order_by('description')
    qs_global_goal_detail = GlobalGoalDetail.objects.filter(
        id_global_goal_period=qs_global_goal_period.pk
    )
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
def goals(request):
    form = GoalsGlobalForm()
    if request.method == 'POST':
        form = GoalsGlobalForm(request.POST)
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

    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')
    qs = Goal.objects.filter(
        Q(description__icontains=q) |
        Q(type__icontains=q) |
        Q(definition__icontains=q) |
        Q(execution__icontains=q)
    ).order_by('description')
    result = pagination(qs, page)

    ctx = {
        'result': result,
        'form': form
    }
    return render(request, 'goals_definition/goals.html', ctx)


@login_required()
def goal(request, id):
    qs = get_object_or_404(Goal, pk=id)
    form = GoalsGlobalForm(instance=qs)

    if request.method == 'POST':
        if request.POST.get('method') == 'edit':
            form = GoalsGlobalForm(request.POST, instance=qs)
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
