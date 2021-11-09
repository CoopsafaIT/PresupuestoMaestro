import json
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from decimal import Decimal as dc

from apps.master_budget.models import MasterParameters
from .models import (
    SavingsLiabilities,
    SavingsLiabilitiesCategory,
    SavingsLiabilitiesComment,
    SavingsLiabilitiesScenario,
    LiabilitiesLoans,
    LiabilitiesLoansCategory,
    LiabilitiesLoansComment,
    LiabilitiesLoansScenario
)
from .forms import (
    SavingsLiabilitiesForm,
    ScenarioCloneForm,
    LiabilitiesLoansScenarioForm,
)
from .calculations import LiabilitiesLoansCalculations
from utils.pagination import pagination
from utils.constants import STATUS_SCENARIO
from utils.sql import execute_sql_query
from utils.constants import (
    LIST_SAVINGS_LIABILITIES_FIELDS,
    LIST_LIABILITIES_LOANS_FIELDS
)


@login_required()
def scenarios_savings_liabilities(request):
    form = SavingsLiabilitiesForm()

    def _correlative(category_name, period, total):
        return (
            f'ESC-{category_name[:4].upper()}-{period}-{total}'
        )

    if request.method == 'POST':
        if request.POST.get('method') == 'create':
            form = SavingsLiabilitiesForm(request.POST)
            if not form.is_valid():
                messages.warning(
                    request,
                    f'Formulario no válido: {form.errors.as_text()}'
                )
            else:
                if request.POST.get('is_active') == 'True':
                    SavingsLiabilitiesScenario.objects.filter(
                        parameter_id=request.POST.get('parameter_id'),
                        category_id=request.POST.get('category_id')
                    ).update(is_active=False)
                _new = form.save()
                _new.period_id = _new.parameter_id.period_id
                _new.created_by = request.user
                _new.updated_by = request.user
                _new.save()
                category_name = _new.category_id.name
                period = _new.parameter_id.period_id.descperiodo
                total = SavingsLiabilitiesScenario.objects.filter(
                    period_id=_new.period_id,
                    category_id=_new.category_id
                ).count()
                correlative = _correlative(category_name, period, total)
                _new.correlative = correlative
                _new.save()

                query = _new.category_id.identifier
                query = f"{query} '{_new.parameter_id.pk}'"
                result = execute_sql_query(query)
                if result.get('status') == 'ok':
                    data = result.get('data')
                    amount = data[0].get('Saldo')
                    _new.base_amount = amount
                    _new.annual_growth_amount = 0
                    _new.save()

                messages.success(
                    request,
                    'Escenario creado con éxito!'
                )
                redirect_url = reverse(
                    'scenario_savings_liabilities', kwargs={'id': _new.pk}
                )
                full_redirect_url = f'{redirect_url}?option=open_calculations_modal'
                return redirect(full_redirect_url)
        elif request.POST.get('method') == 'clone':
            id = request.POST.get('id')
            comment = request.POST.get('comment')
            is_active = request.POST.get('is_active')
            qs_old_esc = get_object_or_404(SavingsLiabilitiesScenario, pk=id)
            _clone = SavingsLiabilitiesScenario.objects.get(pk=id)
            _clone.pk = None
            _clone.save()
            if is_active == 'True':
                SavingsLiabilitiesScenario.objects.filter(
                    parameter_id=_clone.parameter_id.pk,
                    category_id=_clone.category_id.pk
                ).update(is_active=False)
            total = SavingsLiabilitiesScenario.objects.filter(
                period_id=_clone.period_id,
                category_id=_clone.category_id
            ).count()

            _clone.comment = comment
            _clone.is_active = is_active
            _clone.created_by = request.user
            _clone.updated_by = request.user
            _clone.correlative = _correlative(
                _clone.category_id.name,
                _clone.parameter_id.period_id.descperiodo,
                total
            )
            _clone.save()
            _clone.refresh_from_db()
            for item in range(1, 13):
                old_item = SavingsLiabilities.objects.filter(
                    scenario_id=qs_old_esc.pk, month=item
                ).first()
                _upd = SavingsLiabilities.objects.filter(
                    scenario_id=_clone.pk, month=item
                ).first()
                _upd.amount_initial = old_item.amount_initial
                _upd.percent_growth = old_item.percent_growth
                _upd.amount_growth = old_item.amount_growth
                _upd.new_amount = old_item.new_amount
                _upd.rate = old_item.rate
                _upd.total_interest = old_item.total_interest
                _upd.save()
            messages.success(
                request,
                'Escenario clonado con éxito!'
            )
            redirect_url = reverse('scenario_savings_liabilities', kwargs={'id': _clone.pk})
            full_redirect_url = f'{redirect_url}?option=open_calculations_modal'
            return redirect(full_redirect_url)

    page = request.GET.get('page', '')
    parameter = request.GET.get('parameter')
    category = request.GET.get('category')
    status = request.GET.get('status')
    filters = {}
    if not not parameter:
        filters['parameter_id'] = parameter
    if not not category:
        filters['category_id'] = category
    if not not status:
        filters['is_active'] = status
    qs = SavingsLiabilitiesScenario.objects.filter(**filters).exclude(deleted=True).order_by( # NOQA
        'category_id__name',
        '-parameter_id__is_active'
    )
    categories = SavingsLiabilitiesCategory.objects.filter(is_active=True)
    parameters = MasterParameters.objects.filter(is_active=True).order_by(
        '-is_active', 'period_id'
    )
    result = pagination(qs, page=page)
    ctx = {
        'categories': categories,
        'parameters': parameters,
        'status': STATUS_SCENARIO,
        'result': result,
        'form': form
    }
    return render(request, 'savings_liabilities/scenarios.html', ctx)


@login_required()
def scenario_savings_liabilities(request, id):
    qs = get_object_or_404(SavingsLiabilitiesScenario, pk=id)

    def _calculate_interest_generated(amount_initial, new_amount, rate):
        total_amount = (amount_initial + new_amount) / 2
        rate_monthly = rate / 12
        return total_amount * dc(rate_monthly)

    def _save_scenario():
        post = request.POST.copy()
        qs.growth_percentage_january = dc(post.get('growth_percentage_january').replace(',', '')) # NOQA
        qs.growth_percentage_february = dc(post.get('growth_percentage_february').replace(',', '')) # NOQA
        qs.growth_percentage_march = dc(post.get('growth_percentage_march').replace(',', '')) # NOQA
        qs.growth_percentage_april = dc(post.get('growth_percentage_april').replace(',', '')) # NOQA
        qs.growth_percentage_may = dc(post.get('growth_percentage_may').replace(',', ''))
        qs.growth_percentage_june = dc(post.get('growth_percentage_june').replace(',', ''))
        qs.growth_percentage_july = dc(post.get('growth_percentage_july').replace(',', ''))
        qs.growth_percentage_august = dc(post.get('growth_percentage_august').replace(',', '')) # NOQA
        qs.growth_percentage_september = dc(post.get('growth_percentage_september').replace(',', '')) # NOQA
        qs.growth_percentage_october = dc(post.get('growth_percentage_october').replace(',', '')) # NOQA
        qs.growth_percentage_november = dc(post.get('growth_percentage_november').replace(',', '')) # NOQA
        qs.growth_percentage_december = dc(post.get('growth_percentage_december').replace(',', '')) # NOQA

        qs.rate_january = dc(post.get('rate_january').replace(',', ''))
        qs.rate_february = dc(post.get('rate_february').replace(',', ''))
        qs.rate_march = dc(post.get('rate_march').replace(',', ''))
        qs.rate_april = dc(post.get('rate_april').replace(',', ''))
        qs.rate_may = dc(post.get('rate_may').replace(',', ''))
        qs.rate_june = dc(post.get('rate_june').replace(',', ''))
        qs.rate_july = dc(post.get('rate_july').replace(',', ''))
        qs.rate_august = dc(post.get('rate_august').replace(',', ''))
        qs.rate_september = dc(post.get('rate_september').replace(',', ''))
        qs.rate_october = dc(post.get('rate_october').replace(',', ''))
        qs.rate_november = dc(post.get('rate_november').replace(',', ''))
        qs.rate_december = dc(post.get('rate_december').replace(',', ''))
        qs.save()

    if request.method == 'POST':
        if request.POST.get('method') == 'update':
            qs.annual_growth_amount = dc(request.POST.get(
                'annual_growth_amount'
            ).replace(',', ''))
            qs.save()
            annual_growth_amount = qs.annual_growth_amount
            _save_scenario()
            for item in range(1, 13):
                fields = LIST_SAVINGS_LIABILITIES_FIELDS[item-1]
                if item == 1:
                    base_amount = qs.base_amount
                else:
                    qs_before = SavingsLiabilities.objects.get(
                        scenario_id=qs.pk, month=item-1
                    )
                    base_amount = qs_before.new_amount

                growth_percentage = float(
                    request.POST.get(fields.get('growth_percentage'))
                )
                rate = float(request.POST.get(fields.get('rate')))

                _upd = SavingsLiabilities.objects.filter(
                    scenario_id=qs.pk, month=item
                ).first()
                _upd.amount_initial = base_amount
                _upd.percent_growth = growth_percentage
                _upd.amount_growth = annual_growth_amount * dc(growth_percentage / 100)
                _upd.new_amount = _upd.amount_initial + _upd.amount_growth
                _upd.rate = rate
                _upd.total_interest = _calculate_interest_generated(
                    _upd.amount_initial, _upd.amount_growth, _upd.rate
                )
                _upd.save()

        elif request.POST.get('method') == 'change-status':
            if not qs.is_active:
                FinancialInvestmentsScenario.objects.filter(
                    parameter_id=qs.parameter_id.pk,
                    category_id=qs.category_id.pk
                ).update(is_active=False)
            qs.is_active = not qs.is_active
            qs.save()
            message = (
                f'Escenario actualizado a : '
                f'{"Principal" if qs.is_active else "Secundario"}'
                f' con éxito!!'
            )
            messages.success(request, message)

        elif request.POST.get('method') == 'delete':
            qs.is_active = False
            qs.deleted = True
            qs.updated_by = request.user
            qs.save()
            messages.error(request, 'Escenario eliminado')
            return redirect('scenarios_financial_investments')

    qs_detail = SavingsLiabilities.objects.filter(scenario_id=qs.pk).order_by('month')
    ctx = {
        'qs': qs,
        'qs_detail': qs_detail,
        'form_clone': ScenarioCloneForm(),
    }
    return render(request, 'savings_liabilities/scenario.html', ctx)


@login_required()
def scenario_savings_liabilities_comments(request, id):
    if request.is_ajax():
        qs = get_object_or_404(SavingsLiabilitiesScenario, pk=id)
        if request.method == 'POST':
            SavingsLiabilitiesComment.objects.create(
                comment=request.POST.get('comment'),
                created_by=request.user,
                scenario_id=qs,
                deleted=False
            )
        messages = SavingsLiabilitiesComment.objects.values(
            'comment',
            'created_by__username',
            'created_at'
        ).filter(scenario_id=id).order_by('-created_at')
        ctx = {
            'data': list(messages)
        }
        return HttpResponse(json.dumps(ctx, cls=DjangoJSONEncoder))


@login_required()
def scenarios_liabilities_loans(request):
    form = LiabilitiesLoansScenarioForm()

    def _correlative(category_name, period, total):
        return (
            f'ESC-{category_name[:4].upper()}-{period}-{total}'
        )

    if request.method == 'POST':
        if request.POST.get('method') == 'create':
            form = LiabilitiesLoansScenarioForm(request.POST)
            if not form.is_valid():
                messages.warning(
                    request,
                    f'Formulario no válido: {form.errors.as_text()}'
                )
            else:
                if request.POST.get('is_active') == 'True':
                    LiabilitiesLoansScenario.objects.filter(
                        parameter_id=request.POST.get('parameter_id'),
                        category_id=request.POST.get('category_id')
                    ).update(is_active=False)
                _new = form.save()
                _new.period_id = _new.parameter_id.period_id
                _new.created_by = request.user
                _new.updated_by = request.user
                _new.save()
                category_name = _new.category_id.name
                period = _new.parameter_id.period_id.descperiodo
                total = LiabilitiesLoansScenario.objects.filter(
                    period_id=_new.period_id,
                    category_id=_new.category_id
                ).count()
                correlative = _correlative(category_name, period, total)
                _new.correlative = correlative
                _new.save()

                query = (
                    f"[dbo].[sp_pptoMaestroPrestamosCatObtenerSaldoHist] "
                    f"@ParametroId = '{_new.parameter_id.pk}' , "
                    f"@CategoriaId = '{_new.category_id.identifier}' "
                )
                result = execute_sql_query(query)
                if result.get('status') == 'ok':
                    data = result.get('data')
                    amount = data[0].get('Saldo')
                    _new.base_amount = amount
                    _new.annual_growth_amount = 0
                    _new.save()

                messages.success(
                    request,
                    'Escenario creado con éxito!'
                )
                redirect_url = reverse(
                    'scenario_liabilities_loans', kwargs={'id': _new.pk}
                )
                full_redirect_url = f'{redirect_url}?option=open_calculations_modal'
                return redirect(full_redirect_url)
        elif request.POST.get('method') == 'clone':
            id = request.POST.get('id')
            comment = request.POST.get('comment')
            is_active = request.POST.get('is_active')
            qs_old_esc = get_object_or_404(SavingsLiabilitiesScenario, pk=id)
            _clone = SavingsLiabilitiesScenario.objects.get(pk=id)
            _clone.pk = None
            _clone.save()
            if is_active == 'True':
                SavingsLiabilitiesScenario.objects.filter(
                    parameter_id=_clone.parameter_id.pk,
                    category_id=_clone.category_id.pk
                ).update(is_active=False)
            total = SavingsLiabilitiesScenario.objects.filter(
                period_id=_clone.period_id,
                category_id=_clone.category_id
            ).count()

            _clone.comment = comment
            _clone.is_active = is_active
            _clone.created_by = request.user
            _clone.updated_by = request.user
            _clone.correlative = _correlative(
                _clone.category_id.name,
                _clone.parameter_id.period_id.descperiodo,
                total
            )
            _clone.save()
            _clone.refresh_from_db()
            for item in range(1, 13):
                old_item = SavingsLiabilities.objects.filter(
                    scenario_id=qs_old_esc.pk, month=item
                ).first()
                _upd = SavingsLiabilities.objects.filter(
                    scenario_id=_clone.pk, month=item
                ).first()
                _upd.amount_initial = old_item.amount_initial
                _upd.percent_growth = old_item.percent_growth
                _upd.amount_growth = old_item.amount_growth
                _upd.new_amount = old_item.new_amount
                _upd.rate = old_item.rate
                _upd.total_interest = old_item.total_interest
                _upd.save()
            messages.success(
                request,
                'Escenario clonado con éxito!'
            )
            redirect_url = reverse('scenario_liabilities_loans', kwargs={'id': _clone.pk})
            full_redirect_url = f'{redirect_url}?option=open_calculations_modal'
            return redirect(full_redirect_url)

    page = request.GET.get('page', '')
    parameter = request.GET.get('parameter')
    category = request.GET.get('category')
    status = request.GET.get('status')
    filters = {}
    if not not parameter:
        filters['parameter_id'] = parameter
    if not not category:
        filters['category_id'] = category
    if not not status:
        filters['is_active'] = status
    qs = LiabilitiesLoansScenario.objects.filter(**filters).exclude(deleted=True).order_by( # NOQA
        'category_id__name',
        '-parameter_id__is_active'
    )
    categories = LiabilitiesLoansCategory.objects.filter(is_active=True)
    parameters = MasterParameters.objects.filter(is_active=True).order_by(
        '-is_active', 'period_id'
    )
    result = pagination(qs, page=page)
    ctx = {
        'categories': categories,
        'parameters': parameters,
        'status': STATUS_SCENARIO,
        'result': result,
        'form': form
    }
    return render(request, 'liabilities_loans/scenarios.html', ctx)


@login_required()
def scenario_liabilities_loans(request, id):
    qs = get_object_or_404(LiabilitiesLoansScenario, pk=id)

    def _save_scenario():
        post = request.POST.copy()
        qs.growth_percentage_january = dc(post.get('growth_percentage_january').replace(',', '')) # NOQA
        qs.growth_percentage_february = dc(post.get('growth_percentage_february').replace(',', '')) # NOQA
        qs.growth_percentage_march = dc(post.get('growth_percentage_march').replace(',', '')) # NOQA
        qs.growth_percentage_april = dc(post.get('growth_percentage_april').replace(',', '')) # NOQA
        qs.growth_percentage_may = dc(post.get('growth_percentage_may').replace(',', ''))
        qs.growth_percentage_june = dc(post.get('growth_percentage_june').replace(',', ''))
        qs.growth_percentage_july = dc(post.get('growth_percentage_july').replace(',', ''))
        qs.growth_percentage_august = dc(post.get('growth_percentage_august').replace(',', '')) # NOQA
        qs.growth_percentage_september = dc(post.get('growth_percentage_september').replace(',', '')) # NOQA
        qs.growth_percentage_october = dc(post.get('growth_percentage_october').replace(',', '')) # NOQA
        qs.growth_percentage_november = dc(post.get('growth_percentage_november').replace(',', '')) # NOQA
        qs.growth_percentage_december = dc(post.get('growth_percentage_december').replace(',', '')) # NOQA

        qs.rate_january = dc(post.get('rate_january').replace(',', ''))
        qs.rate_february = dc(post.get('rate_february').replace(',', ''))
        qs.rate_march = dc(post.get('rate_march').replace(',', ''))
        qs.rate_april = dc(post.get('rate_april').replace(',', ''))
        qs.rate_may = dc(post.get('rate_may').replace(',', ''))
        qs.rate_june = dc(post.get('rate_june').replace(',', ''))
        qs.rate_july = dc(post.get('rate_july').replace(',', ''))
        qs.rate_august = dc(post.get('rate_august').replace(',', ''))
        qs.rate_september = dc(post.get('rate_september').replace(',', ''))
        qs.rate_october = dc(post.get('rate_october').replace(',', ''))
        qs.rate_november = dc(post.get('rate_november').replace(',', ''))
        qs.rate_december = dc(post.get('rate_december').replace(',', ''))

        qs.term_january = dc(post.get('term_january').replace(',', ''))
        qs.term_february = dc(post.get('term_february').replace(',', ''))
        qs.term_march = dc(post.get('term_march').replace(',', ''))
        qs.term_april = dc(post.get('term_april').replace(',', ''))
        qs.term_may = dc(post.get('term_may').replace(',', ''))
        qs.term_june = dc(post.get('term_june').replace(',', ''))
        qs.term_july = dc(post.get('term_july').replace(',', ''))
        qs.term_august = dc(post.get('term_august').replace(',', ''))
        qs.term_september = dc(post.get('term_september').replace(',', ''))
        qs.term_october = dc(post.get('term_october').replace(',', ''))
        qs.term_november = dc(post.get('term_november').replace(',', ''))
        qs.term_december = dc(post.get('term_december').replace(',', ''))
        qs.save()

    if request.method == 'POST':
        if request.POST.get('method') == 'update':
            calculations = LiabilitiesLoansCalculations()
            qs.annual_growth_amount = dc(request.POST.get(
                'annual_growth_amount'
            ).replace(',', ''))
            qs.save()
            annual_growth_amount = qs.annual_growth_amount
            _save_scenario()
            for item in range(1, 13):
                fields = LIST_LIABILITIES_LOANS_FIELDS[item-1]
                if item == 1:
                    base_amount = qs.base_amount
                else:
                    qs_before = LiabilitiesLoans.objects.get(
                        scenario_id=qs.pk, month=item-1
                    )
                    base_amount = qs_before.new_amount + qs_before.principal_payments

                growth_percentage = float(request.POST.get(fields.get('growth_percentage'))) # NOQA
                rate = float(request.POST.get(fields.get('rate')))
                term = float(request.POST.get(fields.get('term')))

                _upd = LiabilitiesLoans.objects.filter(scenario_id=qs.pk, month=item).first() # NOQA
                _upd.amount_initial = base_amount
                _upd.percent_growth = growth_percentage
                _upd.amount_growth = annual_growth_amount * dc(growth_percentage / 100)
                _upd.rate = rate
                _upd.term = term
                _upd.level_quota = calculations.level_quota(
                    _upd.amount_initial, _upd.amount_growth, _upd.rate, _upd.term
                )
                _upd.total_interest = calculations.total_interest(
                    _upd.amount_initial, _upd.amount_growth, _upd.rate
                )
                _upd.principal_payments = abs(_upd.level_quota) - abs(_upd.total_interest)
                _upd.new_amount = _upd.amount_initial + _upd.amount_growth - _upd.principal_payments # NOQA
                _upd.save()

        elif request.POST.get('method') == 'change-status':
            if not qs.is_active:
                LiabilitiesLoansScenario.objects.filter(
                    parameter_id=qs.parameter_id.pk,
                    category_id=qs.category_id.pk
                ).update(is_active=False)
            qs.is_active = not qs.is_active
            qs.save()
            message = (
                f'Escenario actualizado a : '
                f'{"Principal" if qs.is_active else "Secundario"}'
                f' con éxito!!'
            )
            messages.success(request, message)

        elif request.POST.get('method') == 'delete':
            qs.is_active = False
            qs.deleted = True
            qs.updated_by = request.user
            qs.save()
            messages.error(request, 'Escenario eliminado')
            return redirect('scenarios_liabilities_loans')

    qs_detail = LiabilitiesLoans.objects.filter(scenario_id=qs.pk).order_by('month')
    ctx = {
        'qs': qs,
        'qs_detail': qs_detail,
        'form_clone': ScenarioCloneForm(),
    }
    return render(request, 'liabilities_loans/scenario.html', ctx)


@login_required()
def scenario_liabilities_loans_comments(request, id):
    if request.is_ajax():
        qs = get_object_or_404(LiabilitiesLoansScenario, pk=id)
        if request.method == 'POST':
            LiabilitiesLoansComment.objects.create(
                comment=request.POST.get('comment'),
                created_by=request.user,
                scenario_id=qs,
                deleted=False
            )
        messages = LiabilitiesLoansComment.objects.values(
            'comment',
            'created_by__username',
            'created_at'
        ).filter(scenario_id=id).order_by('-created_at')
        ctx = {
            'data': list(messages)
        }
        return HttpResponse(json.dumps(ctx, cls=DjangoJSONEncoder))
