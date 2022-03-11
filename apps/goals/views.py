import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder


from decimal import Decimal as dc

from utils.pagination import pagination
from .models import (
    GlobalGoalPeriod, GlobalGoalDetail, Goal
)
from .forms import (
    GoalsForm, GoalsGlobalForm, GlobalGoalDetailForm
)

# from utils.sql import execute_sql_query


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

    if request.method == 'POST':
        print(request.POST)
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

    if request.is_ajax():
        if request.method == 'GET':
            goal_id = request.GET.get('goalId')

            qs = Goal.objects.get(pk=goal_id)
            if qs.definition == "A":
                annual_amount = 10000
            else:
                annual_amount = 0
            ctx = {
                'annual_amount': annual_amount,
                'definition': qs.definition
            }
            return HttpResponse(json.dumps(ctx, cls=DjangoJSONEncoder))

        elif request.method == 'POST':
            goal_id = request.POST.get('goalId')
            annual_amount = dc(request.POST.get('annualAmount'))
            data = json.loads(request.POST.get('data'))
            for item in data:
                amount = GlobalGoalDetail.object.get("annual_amount")
                GlobalGoalDetail.objects.filter(
                    id_global_goal_period=id_global_goal_period,
                    goal_id=goal_id,
                    goals_definition=item.get('annual_amount'),
                ).update(amount=amount, annual_amoutn=annual_amount)
            return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder))

    qs_goals = Goal.objects.all().order_by('description')
    qs_global_goal_detail = GlobalGoalDetail.objects.filter(
        id_global_goal_period=qs_global_goal_period.pk
    )
    ctx = {
        'qs_global_goal_period': qs_global_goal_period,
        'qs_goals': qs_goals,
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
