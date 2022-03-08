from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from utils.pagination import pagination
from .models import (GlobalGoalPeriod, Goal)
from.forms import (GoalsForm)


@login_required()
def goals(request):
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
                messages.success(
                    request,
                    'Meta editada con éxito!'
                )
                return redirect('goals_for_period')
    ctx = {
        'form': form
    }
    return render(request, 'goals_period/goals_period_edit.html', ctx)


@login_required()
def goals_detail(request):

    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')
    qs = Goal.objects.filter(Q(description__icontains=q)).order_by('description')
    result = pagination(qs, page)

    ctx = {
        'result': result
    }

    return render(request, 'goals_period/goals_detail.html', ctx)
