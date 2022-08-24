import json
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal as dc

from apps.master_budget.models import MasterParameters
from .models import (
    SavingsLiabilities, SavingsLiabilitiesCategory, SavingsLiabilitiesComment,
    SavingsLiabilitiesScenario, LiabilitiesLoans, LiabilitiesLoansCategory,
    LiabilitiesLoansComment, LiabilitiesLoansScenario, OtherPassivesScenario,
    OtherPassivesCategory, OtherPassives
)
from .forms import (
    SavingsLiabilitiesForm, ScenarioCloneForm, ScenarioCloneUpdateParameterForm,
    LiabilitiesLoansScenarioForm, OthersPassivesScenarioForm, OtherPassivesDefineAmountMonthlyForm
)
from .request_get import QueryGetParms
from .request_post import others_passives_monthly_amount_clean
from .calculations import LiabilitiesLoansCalculations, calculate_interest_generated
from utils.pagination import pagination
from utils.sql import execute_sql_query
from utils.constants import (
    STATUS_SCENARIO, LIST_SAVINGS_LIABILITIES_FIELDS, LIST_LIABILITIES_LOANS_FIELDS,
    OTHERS_ASSETS_CRITERIA
)


@login_required()
def scenarios_savings_liabilities(request):
    form = SavingsLiabilitiesForm()

    def _get_amount_base(query, filter):
        amount = 0
        result = execute_sql_query(f'{query} {filter}')

        if result.get('status') != 'ok':
            return amount
        data = result.get('data')
        amount = data[0].get('Saldo')
        return amount

    def _correlative(category_name, period, total):
        return (f'ESC-{category_name[:4].upper()}-{period}-{total}')

    if request.method == 'POST':
        if request.POST.get('method') == 'create':
            form = SavingsLiabilitiesForm(request.POST)
            if not form.is_valid():
                messages.warning(request, f'Formulario no válido: {form.errors.as_text()}')
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
                _new.correlative = _correlative(category_name, period, total)
                _new.base_amount = _get_amount_base(
                    _new.category_id.identifier, _new.parameter_id.pk
                )
                _new.annual_growth_amount = 0
                _new.save()
                messages.success(request, 'Escenario creado con éxito!')
                redirect_url = reverse('scenario_savings_liabilities', kwargs={'id': _new.pk}) # NOQA
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
            messages.success(request, 'Escenario clonado con éxito!')
            redirect_url = reverse('scenario_savings_liabilities', kwargs={'id': _clone.pk}) # NOQA
            full_redirect_url = f'{redirect_url}?option=open_calculations_modal'
            return redirect(full_redirect_url)

        elif request.POST.get('method') == 'clone-update-parameter':
            id = request.POST.get('id')
            parameter_id = request.POST.get('parameter_id')
            comment = request.POST.get('comment')
            is_active = request.POST.get('is_active')
            qs_parameter = get_object_or_404(MasterParameters, pk=parameter_id)
            qs_old_esc = get_object_or_404(SavingsLiabilitiesScenario, pk=id)
            _clone = SavingsLiabilitiesScenario.objects.get(pk=id)
            _clone.pk = None
            _clone.parameter_id = qs_parameter
            _clone.period_id = qs_parameter.period_id
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
                _clone.parameter_id.period_id.descperiodo, total
            )
            _clone.base_amount = _get_amount_base(
                _clone.category_id.identifier, _clone.parameter_id.pk
            )
            _clone.save()
            _clone.refresh_from_db()
            for item in range(1, 13):
                fields = LIST_SAVINGS_LIABILITIES_FIELDS[item-1]
                if item == 1:
                    base_amount = _clone.base_amount
                else:
                    qs_before = SavingsLiabilities.objects.get(
                        scenario_id=_clone.pk, month=item-1
                    )
                    base_amount = qs_before.new_amount

                growth_percentage = getattr(_clone, fields.get('growth_percentage'), 0)
                rate = getattr(_clone, fields.get('rate'), 0)
                _upd = SavingsLiabilities.objects.filter(
                    scenario_id=_clone.pk, month=item
                ).first()
                _upd.amount_initial = base_amount
                _upd.percent_growth = growth_percentage
                _upd.amount_growth = _clone.annual_growth_amount * dc(growth_percentage / 100) # NOQA
                _upd.new_amount = _upd.amount_initial + _upd.amount_growth
                _upd.rate = rate
                _upd.total_interest = calculate_interest_generated(
                    _upd.amount_initial, _upd.new_amount, _upd.rate
                )
                _upd.save()
            messages.success(
                request, 'Escenario clonado y proyección actualizada con éxito'
            )
            redirect_url = reverse(
                'scenario_savings_liabilities', kwargs={'id': _clone.pk}
            )
            return redirect(redirect_url)

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
        rate_monthly = (rate/100) / 12
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
                    _upd.amount_initial, _upd.new_amount, _upd.rate
                )
                _upd.save()

        elif request.POST.get('method') == 'change-status':
            if not qs.is_active:
                SavingsLiabilitiesScenario.objects.filter(
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
            return redirect('scenarios_savings_liabilities')

    qs_detail = SavingsLiabilities.objects.filter(scenario_id=qs.pk).order_by('month')
    qs_sum = SavingsLiabilities.objects.filter(scenario_id=qs.pk).extra({
        'MontoInicial': 'SUM(MontoInicial)',
        'MontoCrecimiento': 'SUM(MontoCrecimiento)',
        'MontoTotalCrecimiento': 'SUM(MontoTotalCrecimiento)',
        'InteresesGenerado': 'SUM(InteresesGenerado)',
    }).values(
        'MontoInicial', 'MontoCrecimiento',
        'MontoTotalCrecimiento', 'InteresesGenerado',
    )
    ctx = {
        'qs': qs,
        'qs_sum': qs_sum[0],
        'qs_detail': qs_detail,
        'form_clone': ScenarioCloneForm(),
        'form_clone_update': ScenarioCloneUpdateParameterForm()
    }
    return render(request, 'savings_liabilities/scenario.html', ctx)


@login_required()
def scenario_savings_liabilities_comments(request, id):
    if request.is_ajax():
        qs = get_object_or_404(SavingsLiabilitiesScenario, pk=id)
        if request.method == 'POST':
            SavingsLiabilitiesComment.objects.create(
                comment=request.POST.get('comment'), created_by=request.user,
                scenario_id=qs, deleted=False
            )
        messages = SavingsLiabilitiesComment.objects.values(
            'comment', 'created_by__username', 'created_at'
        ).filter(scenario_id=id).order_by('-created_at')
        ctx = {
            'data': list(messages)
        }
        return HttpResponse(json.dumps(ctx, cls=DjangoJSONEncoder))


@login_required()
def scenarios_liabilities_loans(request):
    form = LiabilitiesLoansScenarioForm()

    def _get_amount_base(parameter, identifier):
        amount = 0
        query = (
            f"[dbo].[sp_pptoMaestroPrestamosCatObtenerSaldoHist] "
            f"@ParametroId = '{parameter_id}' ,@CategoriaId = '{identifier}'"
        )
        result = execute_sql_query(query)

        if result.get('status') != 'ok':
            return amount
        data = result.get('data')
        amount = data[0].get('Saldo')
        return amount

    def _correlative(category_name, period, total):
        return (
            f'ESC-{category_name[:4].upper()}-{period}-{total}'
        )

    if request.method == 'POST':
        if request.POST.get('method') == 'create':
            form = LiabilitiesLoansScenarioForm(request.POST)
            if not form.is_valid():
                messages.warning(request, f'Formulario no válido: {form.errors.as_text()}')
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
                _new.correlative = _correlative(category_name, period, total)
                _new.base_amount = _get_amount_base(
                    _new.parameter_id.pk, _new.category_id.identifier
                )
                _new.annual_growth_amount = 0
                _new.save()

                messages.success(request, 'Escenario creado con éxito!')
                redirect_url = reverse(
                    'scenario_liabilities_loans', kwargs={'id': _new.pk}
                )
                full_redirect_url = f'{redirect_url}?option=open_calculations_modal'
                return redirect(full_redirect_url)
        elif request.POST.get('method') == 'clone':
            id = request.POST.get('id')
            comment = request.POST.get('comment')
            is_active = request.POST.get('is_active')
            qs_old_esc = get_object_or_404(LiabilitiesLoansScenario, pk=id)
            _clone = LiabilitiesLoansScenario.objects.get(pk=id)
            _clone.pk = None
            _clone.save()
            if is_active == 'True':
                LiabilitiesLoansScenario.objects.filter(
                    parameter_id=_clone.parameter_id.pk, category_id=_clone.category_id.pk
                ).update(is_active=False)
            total = LiabilitiesLoansScenario.objects.filter(
                period_id=_clone.period_id, category_id=_clone.category_id
            ).count()

            _clone.comment = comment
            _clone.is_active = is_active
            _clone.created_by = request.user
            _clone.updated_by = request.user
            _clone.correlative = _correlative(
                _clone.category_id.name,
                _clone.parameter_id.period_id.descperiodo, total
            )
            _clone.save()
            _clone.refresh_from_db()
            for item in range(1, 13):
                old_item = LiabilitiesLoans.objects.filter(
                    scenario_id=qs_old_esc.pk, month=item
                ).first()
                _upd = LiabilitiesLoans.objects.filter(
                    scenario_id=_clone.pk, month=item
                ).first()

                _upd.amount_initial = old_item.amount_initial
                _upd.percent_growth = old_item.percent_growth
                _upd.amount_growth = old_item.amount_growth
                _upd.rate = old_item.rate
                _upd.term = old_item.term
                _upd.level_quota = old_item.level_quota
                _upd.total_interest = old_item.total_interest
                _upd.principal_payments = old_item.principal_payments
                _upd.new_amount = old_item.new_amount
                _upd.save()

            messages.success(request, 'Escenario clonado con éxito!')
            redirect_url = reverse('scenario_liabilities_loans', kwargs={'id': _clone.pk})
            full_redirect_url = f'{redirect_url}?option=open_calculations_modal'
            return redirect(full_redirect_url)

        elif request.POST.get('method') == "clone-update-parameter":
            calculations = LiabilitiesLoansCalculations()
            id = request.POST.get('id')
            parameter_id = request.POST.get('parameter_id')
            comment = request.POST.get('comment')
            is_active = request.POST.get('is_active')
            qs_parameter = get_object_or_404(MasterParameters, pk=parameter_id)
            qs_old_esc = get_object_or_404(LiabilitiesLoansScenario, pk=id)
            _clone = LiabilitiesLoansScenario.objects.get(pk=id)
            _clone.pk = None
            _clone.parameter_id = qs_parameter
            _clone.period_id = qs_parameter.period_id
            _clone.save()
            if is_active == 'True':
                LiabilitiesLoansScenario.objects.filter(
                    parameter_id=_clone.parameter_id.pk, category_id=_clone.category_id.pk
                ).update(is_active=False)
            total = LiabilitiesLoansScenario.objects.filter(
                period_id=_clone.period_id, category_id=_clone.category_id
            ).count()

            _clone.comment = comment
            _clone.is_active = is_active
            _clone.created_by = request.user
            _clone.updated_by = request.user
            _clone.correlative = _correlative(
                _clone.category_id.name, _clone.parameter_id.period_id.descperiodo, total
            )
            _clone.base_amount = _get_amount_base(
                _clone.parameter_id.pk, _clone.category_id.identifier
            )
            _clone.save()
            _clone.refresh_from_db()
            for item in range(1, 13):
                fields = LIST_LIABILITIES_LOANS_FIELDS[item-1]
                if item == 1:
                    base_amount = _clone.base_amount
                    principal_payments_before = 0
                else:
                    qs_before = LiabilitiesLoans.objects.get(scenario_id=_clone.pk, month=item-1) # NOQA
                    base_amount = qs_before.new_amount
                    principal_payments_before = qs_before.principal_payments

                growth_percentage = getattr(_clone, fields.get('growth_percentage'), 0)
                rate = getattr(_clone, fields.get('rate'), 0)
                term = getattr(_clone, fields.get('term'), 0)

                _upd = LiabilitiesLoans.objects.filter(scenario_id=_clone.pk, month=item).first() # NOQA
                _upd.amount_initial = base_amount
                _upd.percent_growth = growth_percentage
                _upd.amount_growth = (
                    _clone.annual_growth_amount * dc(growth_percentage / 100)
                ) + principal_payments_before
                _upd.rate = rate
                _upd.term = term
                _upd.level_quota = calculations.level_quota(
                    _upd.amount_initial, _upd.amount_growth, _upd.rate, _upd.term
                )
                _upd.total_interest = calculations.total_interest(
                    _upd.amount_initial, _upd.amount_growth, _upd.rate
                )
                _upd.principal_payments = abs(_upd.level_quota) - abs(_upd.total_interest)
                if item == 12:
                    _upd.new_amount = _upd.amount_initial + _upd.amount_growth - 0
                else:
                    _upd.new_amount = _upd.amount_initial + _upd.amount_growth - _upd.principal_payments # NOQA
                _upd.save()
            messages.success(request, 'Escenario clonado y proyección actualizada con éxito') # NOQA
            redirect_url = reverse('scenario_liabilities_loans', kwargs={'id': _clone.pk})
            return redirect(redirect_url)

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
                    principal_payments_before = 0
                else:
                    qs_before = LiabilitiesLoans.objects.get(
                        scenario_id=qs.pk, month=item-1
                    )
                    base_amount = qs_before.new_amount
                    principal_payments_before = qs_before.principal_payments

                growth_percentage = float(request.POST.get(fields.get('growth_percentage'))) # NOQA
                rate = float(request.POST.get(fields.get('rate')))
                term = float(request.POST.get(fields.get('term')))
                _upd = LiabilitiesLoans.objects.filter(scenario_id=qs.pk, month=item).first() # NOQA
                _upd.amount_initial = base_amount
                _upd.percent_growth = growth_percentage
                _upd.amount_growth = (
                    annual_growth_amount * dc(growth_percentage / 100)
                ) + principal_payments_before
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
                f'{"Principal" if qs.is_active else "Secundario"} con éxito!'
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
    qs_sum = LiabilitiesLoans.objects.filter(scenario_id=qs.pk).extra({
        'MontoInicial': 'SUM(MontoInicial)',
        'MontoCrecimiento': 'SUM(MontoCrecimiento)',
        'PagosCapital': 'SUM(PagosCapital)',
        'MontoTotalCrecimiento': 'SUM(MontoTotalCrecimiento)',
        'CuotaNivelada': 'SUM(CuotaNivelada)',
        'InteresesPagados': 'SUM(InteresesPagados)',
    }).values(
        'MontoInicial', 'MontoCrecimiento', 'PagosCapital',
        'MontoTotalCrecimiento', 'CuotaNivelada', 'InteresesPagados'
    )
    ctx = {
        'qs': qs,
        'qs_detail': qs_detail,
        'qs_sum': qs_sum[0],
        'form_clone': ScenarioCloneForm(),
        'form_clone_update': ScenarioCloneUpdateParameterForm()
    }
    return render(request, 'liabilities_loans/scenario.html', ctx)


@login_required()
def scenario_liabilities_loans_comments(request, id):
    if request.is_ajax():
        qs = get_object_or_404(LiabilitiesLoansScenario, pk=id)
        if request.method == 'POST':
            LiabilitiesLoansComment.objects.create(
                comment=request.POST.get('comment'), created_by=request.user,
                scenario_id=qs, deleted=False
            )
        messages = LiabilitiesLoansComment.objects.values(
            'comment', 'created_by__username', 'created_at'
        ).filter(scenario_id=id).order_by('-created_at')
        ctx = {
            'data': list(messages)
        }
        return HttpResponse(json.dumps(ctx, cls=DjangoJSONEncoder))


@login_required()
def scenarios_others_passives(request):
    form = OthersPassivesScenarioForm()

    def _correlative(period, total):
        return f'ESC-{period}-{total}'

    if request.POST:
        if request.POST.get('method') == 'create':
            form = OthersPassivesScenarioForm(request.POST)
            if not form.is_valid():
                messages.warning(request, f'Formulario no válido: {form.errors.as_text()}')
            else:
                if request.POST.get('is_active') == 'True':
                    OtherPassivesScenario.objects.filter(
                        parameter_id=request.POST.get('parameter_id')
                    ).update(is_active=False)
                _new = form.save()
                _new.period_id = _new.parameter_id.period_id
                _new.created_by = request.user
                _new.updated_by = request.user
                _new.save()
                _new.correlative = _correlative(
                    _new.parameter_id.period_id.descperiodo,
                    OtherPassivesScenario.objects.filter(
                        period_id=_new.period_id
                    ).count()
                )
                _new.save()
                messages.success(request, 'Escenario creado con éxito!')
                for qs_category in OtherPassivesCategory.objects.filter(is_active=True):
                    query = f"{qs_category.identifier} '{_new.parameter_id.pk}'"
                    result = execute_sql_query(query)
                    if result.get('status') == 'ok':
                        for item in result.get('data'):
                            OtherPassives.objects.create(
                                scenario_id=_new,
                                category_id=qs_category,
                                category=item.get('CategoriaId', 0),
                                category_name=item.get('Categoria', ''),
                                previous_balance=item.get('Saldo', 0),
                                percentage=0,
                                new_balance=0,
                                amount_january=item.get('Saldo', 0),
                                amount_february=item.get('Saldo', 0),
                                amount_march=item.get('Saldo', 0),
                                amount_april=item.get('Saldo', 0),
                                amount_may=item.get('Saldo', 0),
                                amount_june=item.get('Saldo', 0),
                                amount_july=item.get('Saldo', 0),
                                amount_august=item.get('Saldo', 0),
                                amount_september=item.get('Saldo', 0),
                                amount_october=item.get('Saldo', 0),
                                amount_november=item.get('Saldo', 0),
                                amount_december=item.get('Saldo', 0)
                            )
                    else:
                        messages.danger(
                            request, f'No se pudo extraer información Historica de categoria: {qs_category}' # NOQA
                        )
                redirect_url = reverse('scenario_others_passives', kwargs={'id': _new.pk})
                full_redirect_url = f'{redirect_url}?option='
                return redirect(full_redirect_url)
        elif request.POST.get('method') == 'clone':
            id = request.POST.get('id')
            comment = request.POST.get('comment')
            is_active = request.POST.get('is_active')
            qs_old_esc = get_object_or_404(OtherPassivesScenario, pk=id)
            _clone = OtherPassivesScenario.objects.get(pk=id)
            _clone.pk = None
            _clone.save()
            if is_active == 'True':
                OtherPassivesScenario.objects.filter(
                    parameter_id=_clone.parameter_id.pk
                ).update(is_active=False)
            _clone.comment = comment
            _clone.is_active = is_active
            _clone.created_by = request.user
            _clone.updated_by = request.user
            _clone.correlative = _correlative(
                _clone.parameter_id.period_id.descperiodo,
                OtherPassivesScenario.objects.filter(
                    period_id=_clone.period_id
                ).count()
            )
            _clone.save()
            _clone.refresh_from_db()
            for item_category in OtherPassives.objects.filter(scenario_id=qs_old_esc.pk):
                _new = OtherPassives.objects.get(pk=item_category.pk)
                _new.pk = None
                _new.save()
                _new.scenario_id = _clone
                _new.save()
            messages.success(request, 'Escenario clonado con éxito!')
            redirect_url = reverse(
                'scenario_others_passives', kwargs={'id': _clone.pk}
            )
            full_redirect_url = f'{redirect_url}?option='
            return redirect(full_redirect_url)

    query_parms = QueryGetParms(request.GET)
    filters = query_parms.get_query_filters()
    qs = OtherPassivesScenario.objects.filter(**filters).exclude(deleted=True).order_by(
        '-parameter_id__is_active', 'correlative'
    )
    parameters = MasterParameters.objects.filter(is_active=True).order_by(
        '-is_active', 'period_id'
    )
    result = pagination(qs, page=query_parms.get_page())
    ctx = {
        'parameters': parameters,
        'status': STATUS_SCENARIO,
        'result': result,
        'form': form
    }
    return render(request, 'others_passives/scenarios.html', ctx)


@login_required()
def scenario_others_passives(request, id):
    qs = get_object_or_404(OtherPassivesScenario, pk=id)
    qs_categories = OtherPassivesCategory.objects.all().order_by('name')
    qs_details = OtherPassives.objects.filter(scenario_id=qs.pk).order_by(
        'category_id', 'category'
    )

    def _struct_data_by_order():
        data = []
        for category in qs_categories:
            category_sum = qs_details.filter(category_id=category.pk).aggregate(sum_total=Sum('new_balance')) # NOQA
            data.append({
                'category_name': category.name,
                'sub_categories': qs_details.filter(category_id=category.pk),
                'category_sum': category_sum.get('sum_total', 0)
            })
        return data

    if request.method == 'POST':
        if request.POST.get('method') == 'criteria':
            item = get_object_or_404(OtherPassives, pk=request.POST.get('pk'))
            item.comment = request.POST.get('comment', '')
            item.percentage = request.POST.get('percentage').replace(',', '')
            item.new_balance = request.POST.get('new_balance').replace(',', '')
            item.criteria = request.POST.get('criteria')
            item.save()
            messages.success(request, "Actualización realizada con éxito!")
        elif request.POST.get('method') == 'define-monthly-by-amount':
            qs_item = get_object_or_404(OtherPassives, pk=request.POST.get('pk'))
            data = others_passives_monthly_amount_clean(request.POST)
            form = OtherPassivesDefineAmountMonthlyForm(data, instance=qs_item)
            if not form.is_valid():
                messages.warning(request, f'Formulario no válido: {form.errors.as_text()}')
            else:
                OtherPassives.objects.filter(pk=qs_item.pk).update(**form.cleaned_data)
                messages.success(request, "Actualización realizada con éxito!")
        elif request.POST.get('method') == 'change-status':
            if not qs.is_active:
                OtherPassivesScenario.objects.filter(
                    parameter_id=qs.parameter_id.pk
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
            return redirect('scenarios_others_passives')

    ctx = {
        'qs': qs,
        'qs_details': _struct_data_by_order(),
        'others_assets_criteria': OTHERS_ASSETS_CRITERIA,
        'form_clone': ScenarioCloneForm()
    }
    return render(request, 'others_passives/scenario.html', ctx)
