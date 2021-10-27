import json
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal as dc

from .models import (
    LoanPortfolioScenario,
    LoanPortfolioCategory,
    LoanPortfolioCategoryMap,
    LoanPortfolioComment,
    LoanPortfolio,
    FinancialInvestmentsCategory,
    FinancialInvestments,
    FinancialInvestmentsComment,
    FinancialInvestmentsScenario
)
from .forms import (
    LoanPortfolioScenarioForm,
    ScenarioCloneForm,
    FinancialInvestmentsScenarioForm,
    FinancialInvestmentsScenarioCloneForm,
)
from apps.master_budget.models import MasterParameters
from utils.pagination import pagination
from utils.constants import (
    STATUS_SCENARIO,
    LIST_LOAN_PORTFOLIO_FIELDS,
    LIST_FINANCIAL_INVESTMENTS_FIELDS
)
from utils.sql import execute_sql_query
from .calculations import LoanPortfolioCalculations


@login_required()
def categories_loan_portfolio(request):
    def _execute_category():
        query = 'EXEC dbo.sp_pptoMaestroCarteraCredCatObtenerCatalogo'
        return execute_sql_query(query)

    def _execute_type():
        query = 'EXEC dbo.sp_pptoMaestroCarteraCredCatTipoPrestamoObtenerCatalogo'
        return execute_sql_query(query)

    def _find_data():
        category = request.POST.get('category')
        types_of_loans = request.POST.getlist('types_of_loans[]')
        category_dict = {}
        types_list = []
        result_categories = _execute_category()
        result_types = _execute_type()
        categories = result_categories.get('data')
        types = result_types.get('data')
        for item in categories:
            if str(item.get('Id')) == category:
                category_dict = item

        for item in types:
            if str(item.get('Id')) in types_of_loans:
                types_list.append(item)

        return category_dict, types_list

    if request.is_ajax():
        result = _execute_type()
        data = []
        if result.get('status') == 'ok':
            codes = list(LoanPortfolioCategoryMap.objects.values_list('code', flat=True))
            data = list(result.get('data'))
            for key, value in enumerate(data):
                if value.get('Id') in codes:
                    data.pop(key)
        ctx = {
            'data': data
        }
        return HttpResponse(json.dumps(ctx, cls=DjangoJSONEncoder))

    if request.method == 'POST':
        category, types_of_loans = _find_data()
        _new_cat = LoanPortfolioCategory()
        _new_cat.code_core = int(category.get('Id'))
        _new_cat.name = category.get('Nombre')
        _new_cat.is_active = True
        _new_cat.identifier = category.get('Identificador')
        _new_cat.created_by = request.user
        _new_cat.updated_by = request.user
        _new_cat.save()

        for item in types_of_loans:
            LoanPortfolioCategoryMap.objects.create(
                category_id=_new_cat,
                name=item.get('Nombre'),
                code=item.get('Id'),
                created_by=request.user,
                updated_by=request.user
            )
        messages.success(request, 'Categoria agregada con éxito!')

    result = _execute_category()
    categories = []
    if not result.get('status') == 'ok':
        messages.warning(request, 'No se cargaron categorias desde Core')
    else:
        categories_result = result.get('data')
        codes = list(LoanPortfolioCategory.objects.values_list('code_core', flat=True))
        for key, value in enumerate(categories_result):
            if int(value.get('Id')) not in codes:
                categories.append(value)

    qs_categories = LoanPortfolioCategory.objects.all()
    ctx = {
        'qs_categories': qs_categories,
        'categories': categories
    }
    return render(request, 'loan_portfolio/category/list.html', ctx)


@login_required()
def category_loan_portfolio(request, id):
    qs = get_object_or_404(LoanPortfolioCategory, pk=id)

    def _execute_type():
        query = 'EXEC dbo.sp_pptoMaestroCarteraCredCatTipoPrestamoObtenerCatalogo'
        return execute_sql_query(query)

    def _find_data():
        types_of_loans = request.POST.getlist('types_of_loans[]')
        types_list = []
        result_types = _execute_type()
        types = result_types.get('data')

        for item in types:
            if str(item.get('Id')) in types_of_loans:
                types_list.append(item)
        return types_list

    if request.method == 'POST':
        types_of_loans = _find_data()
        LoanPortfolioCategoryMap.objects.filter(category_id=qs.pk).delete()
        for item in types_of_loans:
            LoanPortfolioCategoryMap.objects.create(
                category_id=qs,
                name=item.get('Nombre'),
                code=item.get('Id'),
                created_by=request.user,
                updated_by=request.user
            )
        messages.success(request, 'Categoria editada con éxito!')

    qs_detail = LoanPortfolioCategoryMap.objects.filter(
        category_id=qs.pk
    ).values_list('code', flat=True)

    result = _execute_type()

    ctx = {
        'qs': qs,
        'qs_detail': qs_detail,
        'result': result.get('data')
    }
    return render(request, 'loan_portfolio/category/edit.html', ctx)


@login_required()
def scenarios_loan_portfolio(request):
    form = LoanPortfolioScenarioForm()

    def _correlative(category_name, period, total):
        return (
            f'ESC-{category_name[:4].upper()}-{period}-{total}'
        )

    if request.method == 'POST':
        if request.POST.get('method') == 'create':
            form = LoanPortfolioScenarioForm(request.POST)
            if not form.is_valid():
                messages.warning(
                    request,
                    f'Formulario no válido: {form.errors.as_text()}'
                )
            else:
                if request.POST.get('is_active') == 'True':
                    LoanPortfolioScenario.objects.filter(
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
                total = LoanPortfolioScenario.objects.filter(
                    period_id=_new.period_id,
                    category_id=_new.category_id
                ).count()
                correlative = _correlative(category_name, period, total)
                _new.correlative = correlative
                _new.save()
                query = (
                    f'EXEC dbo.sp_pptoMaestroCarteraCredCatObtenerSaldoCarteraHist '
                    f'@ParametroId = {_new.parameter_id.pk}, '
                    f'@CategoriaId = {_new.category_id.pk}'
                )
                result = execute_sql_query(query)
                if result.get('status') == 'ok':
                    data = result.get('data')
                    amount = data[0].get('SaldoCartera')
                    _new.base_amount = amount
                    _new.annual_growth_percentage = 0
                    _new.annual_growth_amount = 0
                    _new.save()

                messages.success(
                    request,
                    'Escenario creado con éxito!'
                )
                redirect_url = reverse('scenario_loan_portfolio', kwargs={'id': _new.pk})
                full_redirect_url = f'{redirect_url}?option=open_calculations_modal'
                return redirect(full_redirect_url)
        elif request.POST.get('method') == 'clone':
            id = request.POST.get('id')
            comment = request.POST.get('comment')
            is_active = request.POST.get('is_active')
            qs_old_esc = get_object_or_404(LoanPortfolioScenario, pk=id)
            _clone = LoanPortfolioScenario.objects.get(pk=id)
            _clone.pk = None
            _clone.save()
            if is_active == 'True':
                LoanPortfolioScenario.objects.filter(
                    parameter_id=_clone.parameter_id.pk,
                    category_id=_clone.category_id.pk
                ).update(is_active=False)
            total = LoanPortfolioScenario.objects.filter(
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
                old_item = LoanPortfolio.objects.filter(
                    scenario_id=qs_old_esc.pk, month=item
                ).first()
                _upd = LoanPortfolio.objects.filter(
                    scenario_id=_clone.pk, month=item
                ).first()
                _upd.amount_initial = old_item.amount_initial
                _upd.percent_growth = old_item.percent_growth
                _upd.amount_growth = old_item.amount_growth
                _upd.rate = old_item.rate
                _upd.term = old_item.term
                _upd.percentage_arrears = old_item.percentage_arrears
                _upd.commission_percentage = old_item.commission_percentage
                _upd.level_quota = old_item.level_quota
                _upd.total_interest = old_item.total_interest
                _upd.principal_payments = old_item.principal_payments
                _upd.new_amount = old_item.new_amount
                _upd.commission_amount = old_item.commission_amount
                _upd.amount_arrears = old_item.amount_arrears
                _upd.default_interest = old_item.default_interest
                _upd.save()
            messages.success(
                request,
                'Escenario clonado con éxito!'
            )
            redirect_url = reverse('scenario_loan_portfolio', kwargs={'id': _clone.pk})
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
    qs = LoanPortfolioScenario.objects.filter(**filters).exclude(deleted=True).order_by(
        'category_id__name',
        '-parameter_id__is_active'
    )
    categories = LoanPortfolioCategory.objects.filter(is_active=True)
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
    return render(request, 'loan_portfolio/scenarios.html', ctx)


@login_required()
def scenario_loan_portfolio(request, id):
    qs = get_object_or_404(LoanPortfolioScenario, pk=id)

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

        qs.percentage_arrears_january = dc(post.get('percentage_arrears_january').replace(',','')) # NOQA
        qs.percentage_arrears_february = dc(post.get('percentage_arrears_february').replace(',','')) # NOQA
        qs.percentage_arrears_march = dc(post.get('percentage_arrears_march').replace(',','')) # NOQA
        qs.percentage_arrears_april = dc(post.get('percentage_arrears_april').replace(',','')) # NOQA
        qs.percentage_arrears_may = dc(post.get('percentage_arrears_may').replace(',','')) # NOQA
        qs.percentage_arrears_june = dc(post.get('percentage_arrears_june').replace(',','')) # NOQA
        qs.percentage_arrears_july = dc(post.get('percentage_arrears_july').replace(',','')) # NOQA
        qs.percentage_arrears_august = dc(post.get('percentage_arrears_august').replace(',','')) # NOQA
        qs.percentage_arrears_september = dc(post.get('percentage_arrears_september').replace(',','')) # NOQA
        qs.percentage_arrears_october = dc(post.get('percentage_arrears_october').replace(',','')) # NOQA
        qs.percentage_arrears_november = dc(post.get('percentage_arrears_november').replace(',','')) # NOQA
        qs.percentage_arrears_december = dc(post.get('percentage_arrears_december').replace(',','')) # NOQA

        qs.commission_percentage_january = dc(post.get('commission_percentage_january').replace(',','')) # NOQA
        qs.commission_percentage_february = dc(post.get('commission_percentage_february').replace(',','')) # NOQA
        qs.commission_percentage_march = dc(post.get('commission_percentage_march').replace(',','')) # NOQA
        qs.commission_percentage_april = dc(post.get('commission_percentage_april').replace(',','')) # NOQA
        qs.commission_percentage_may = dc(post.get('commission_percentage_may').replace(',','')) # NOQA
        qs.commission_percentage_june = dc(post.get('commission_percentage_june').replace(',','')) # NOQA
        qs.commission_percentage_july = dc(post.get('commission_percentage_july').replace(',','')) # NOQA
        qs.commission_percentage_august = dc(post.get('commission_percentage_august').replace(',','')) # NOQA
        qs.commission_percentage_september = dc(post.get('commission_percentage_september').replace(',','')) # NOQA
        qs.commission_percentage_october = dc(post.get('commission_percentage_october').replace(',','')) # NOQA
        qs.commission_percentage_november = dc(post.get('commission_percentage_november').replace(',','')) # NOQA
        qs.commission_percentage_december = dc(post.get('commission_percentage_december').replace(',','')) # NOQA
        qs.save()

    if request.method == 'POST':
        if request.POST.get('method') == 'update':
            calculations = LoanPortfolioCalculations()
            qs.annual_growth_percentage = dc(request.POST.get('annual_growth_percentage').replace(',','')) # NOQA
            qs.annual_growth_amount = dc(request.POST.get('annual_growth_amount').replace(',','')) # NOQA
            qs.save()
            _save_scenario()
            for item in range(1, 13):
                fields = LIST_LOAN_PORTFOLIO_FIELDS[item-1]
                growth_percentage = request.POST.get(fields.get('growth_percentage'))
                percentage_arrears = request.POST.get(fields.get('percentage_arrears'))
                commission_percentage = request.POST.get(fields.get('commission_percentage')) # NOQA
                rate = request.POST.get(fields.get('rate'))
                term = request.POST.get(fields.get('term'))
                if item == 1:
                    base_amount = qs.base_amount
                    principal_payments_before = 0
                else:
                    qs_before = LoanPortfolio.objects.get(
                        scenario_id=qs.pk, month=item-1
                    )
                    base_amount = qs_before.new_amount
                    principal_payments_before = qs_before.principal_payments

                growth_percentage = float(growth_percentage)
                _upd = LoanPortfolio.objects.filter(scenario_id=qs.pk, month=item).first()
                _upd.amount_initial = base_amount
                _upd.percent_growth = growth_percentage
                amount_growth = (
                    qs.annual_growth_amount * (dc(growth_percentage) / 100)
                ) + principal_payments_before
                _upd.amount_growth = amount_growth
                _upd.rate = float(rate)
                _upd.term = float(term)
                _upd.percentage_arrears = float(percentage_arrears)
                _upd.commission_percentage = float(commission_percentage)
                level_quota = calculations.level_quota(
                    _upd.amount_initial, _upd.amount_growth, _upd.rate, _upd.term
                )
                _upd.level_quota = level_quota
                _upd.total_interest = calculations.total_interest(
                    _upd.amount_initial, _upd.amount_growth, _upd.rate
                )
                _upd.principal_payments = abs(_upd.level_quota) - abs(_upd.total_interest)
                _upd.new_amount = calculations.new_amount(
                    _upd.amount_initial, _upd.amount_growth, _upd.principal_payments
                )
                _upd.commission_amount = calculations.commission_amount(
                    _upd.amount_growth, dc(_upd.commission_percentage)
                )
                _upd.amount_arrears = calculations.amount_arrears(
                    _upd.new_amount, _upd.percentage_arrears
                )
                _upd.default_interest = calculations.default_interest(
                    _upd.amount_arrears, _upd.rate
                )
                _upd.save()
            messages.success(
                request,
                'Escenario editado con éxito!'
            )
        elif request.POST.get('method') == 'change-status':
            if not qs.is_active:
                LoanPortfolioScenario.objects.filter(
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
            return redirect('scenarios_loan_portfolio')

    qs_detail = LoanPortfolio.objects.filter(scenario_id=qs.pk).order_by('month')
    ctx = {
        'qs': qs,
        'qs_detail': qs_detail,
        'form_clone': ScenarioCloneForm()
    }
    return render(request, 'loan_portfolio/scenario.html', ctx)


@login_required()
def scenario_loan_portfolio_comments(request, id):
    if request.is_ajax():
        qs = get_object_or_404(LoanPortfolioScenario, pk=id)
        if request.method == 'POST':
            LoanPortfolioComment.objects.create(
                comment=request.POST.get('comment'),
                created_by=request.user,
                scenario_id=qs,
                deleted=False
            )
        messages = LoanPortfolioComment.objects.values(
            'comment',
            'created_by__username',
            'created_at'
        ).filter(scenario_id=id).order_by('-created_at')
        ctx = {
            'data': list(messages)
        }
        return HttpResponse(json.dumps(ctx, cls=DjangoJSONEncoder))


@login_required()
def scenarios_financial_investments(request):
    form = FinancialInvestmentsScenarioForm()

    def _correlative(category_name, period, total):
        return (
            f'ESC-{category_name[:4].upper()}-{period}-{total}'
        )

    if request.method == 'POST':
        if request.POST.get('method') == 'create':
            form = FinancialInvestmentsScenarioForm(request.POST)
            if not form.is_valid():
                messages.warning(
                    request,
                    f'Formulario no válido: {form.errors.as_text()}'
                )
            else:
                if request.POST.get('is_active') == 'True':
                    FinancialInvestmentsScenario.objects.filter(
                        parameter_id=request.POST.get('parameter_id'),
                        category_id=request.POST.get('category_id')
                    ).update(is_active=False)
                _new = form.save()
                _new.period_id = _new.parameter_id.period_id
                _new.created_by = request.user
                _new.updated_by = request.user
                _new.save()
                total = FinancialInvestmentsScenario.objects.filter(
                    period_id=_new.period_id,
                    category_id=_new.category_id
                ).count()
                correlative = _correlative(
                    _new.category_id.name,
                    _new.parameter_id.period_id.descperiodo,
                    total
                )
                _new.correlative = correlative
                _new.save()
                query = (
                    f"EXEC dbo.sp_pptoMaestroInversionesFinacierasObtenerSaldoActualHist "
                    f"@ParametroId = {_new.parameter_id.pk}, "
                    f"@TipoInversionId = {_new.category_id.identifier}, "
                    f"@Estado = '0'"
                )
                result = execute_sql_query(query)
                if result.get('status') == 'ok':
                    data = result.get('data')
                    amount = data[0].get('ValorTitulo')
                    _new.base_amount = amount
                    _new.save()

                messages.success(
                    request,
                    'Escenario creado con éxito!'
                )
                redirect_url = reverse(
                    'scenario_financial_investments', kwargs={'id': _new.pk}
                )
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
    qs = FinancialInvestmentsScenario.objects.filter(**filters).exclude(
        deleted=True
    ).order_by(
        'category_id__name',
        '-parameter_id__is_active'
    )
    categories = FinancialInvestmentsCategory.objects.filter(is_active=True)
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
    return render(request, 'financial_investments/scenarios.html', ctx)


@login_required()
def scenario_financial_investments(request, id):
    qs = get_object_or_404(FinancialInvestmentsScenario, pk=id)

    def _save_scenario():
        post = request.POST.copy()
        qs.increases_january = dc(post.get('increases_january').replace(',', ''))
        qs.increases_february = dc(post.get('increases_february').replace(',', ''))
        qs.increases_march = dc(post.get('increases_march').replace(',', ''))
        qs.increases_april = dc(post.get('increases_april').replace(',', ''))
        qs.increases_may = dc(post.get('increases_may').replace(',', ''))
        qs.increases_june = dc(post.get('increases_june').replace(',', ''))
        qs.increases_july = dc(post.get('increases_july').replace(',', ''))
        qs.increases_august = dc(post.get('increases_august').replace(',', ''))
        qs.increases_september = dc(post.get('increases_september').replace(',', ''))
        qs.increases_october = dc(post.get('increases_october').replace(',', ''))
        qs.increases_november = dc(post.get('increases_november').replace(',', ''))
        qs.increases_december = dc(post.get('increases_december').replace(',', ''))

        qs.decreases_january = dc(post.get('decreases_january').replace(',', ''))
        qs.decreases_february = dc(post.get('decreases_february').replace(',', ''))
        qs.decreases_march = dc(post.get('decreases_march').replace(',', ''))
        qs.decreases_april = dc(post.get('decreases_april').replace(',', ''))
        qs.decreases_may = dc(post.get('decreases_may').replace(',', ''))
        qs.decreases_june = dc(post.get('decreases_june').replace(',', ''))
        qs.decreases_july = dc(post.get('decreases_july').replace(',', ''))
        qs.decreases_august = dc(post.get('decreases_august').replace(',', ''))
        qs.decreases_september = dc(post.get('decreases_september').replace(',', ''))
        qs.decreases_october = dc(post.get('decreases_october').replace(',', ''))
        qs.decreases_november = dc(post.get('decreases_november').replace(',', ''))
        qs.decreases_december = dc(post.get('decreases_december').replace(',', ''))

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
            _save_scenario()
            for item in range(1, 13):
                fields = LIST_FINANCIAL_INVESTMENTS_FIELDS[item-1]
                if item == 1:
                    base_amount = qs.base_amount
                else:
                    qs_before = FinancialInvestments.objects.get(
                        scenario_id=qs.pk, month=item-1
                    )
                    base_amount = qs_before.new_amount
                increases = dc(request.POST.get(fields.get('increases')))
                decreases = dc(request.POST.get(fields.get('decreases')))
                rate = float(request.POST.get(fields.get('rate')))

                _upd = FinancialInvestments.objects.filter(
                    scenario_id=qs.pk, month=item
                ).first()
                _upd.amount_initial = base_amount
                _upd.amount_increase = increases
                _upd.amount_decrease = decreases
                _upd.new_amount = base_amount + increases - decreases
                _upd.rate = rate
                _upd.amount_interest_earned = _upd.new_amount * dc(rate / 12 / 100)
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

    form = FinancialInvestmentsScenarioCloneForm()
    qs_detail = FinancialInvestments.objects.filter(scenario_id=qs.pk).order_by('month')
    ctx = {
        'qs': qs,
        'qs_detail': qs_detail,
        'form': form,
    }
    return render(request, 'financial_investments/scenario.html', ctx)


@login_required()
def scenario_financial_investments_comments(request, id):
    if request.is_ajax():
        qs = get_object_or_404(FinancialInvestmentsScenario, pk=id)
        if request.method == 'POST':
            FinancialInvestmentsComment.objects.create(
                comment=request.POST.get('comment'),
                created_by=request.user,
                scenario_id=qs,
                deleted=False
            )
        messages = FinancialInvestmentsComment.objects.values(
            'comment',
            'created_by__username',
            'created_at'
        ).filter(scenario_id=id).order_by('-created_at')
        ctx = {
            'data': list(messages)
        }
        return HttpResponse(json.dumps(ctx, cls=DjangoJSONEncoder))
