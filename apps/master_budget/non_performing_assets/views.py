import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.exceptions import PermissionDenied
# from decimal import Decimal as dc

from apps.master_budget.models import MasterParameters
from utils.constants import STATUS_SCENARIO, OTHERS_ASSETS_CRITERIA, MONTH_CHOICES
from apps.main.models import Detallexpresupuestoinversion
from .models import (
    NonPerformingAssetsScenario,
    NonPerformingAssetsXCategory,
    BudgetedNonProductiveAssets,
    NonPerformingAssetsCategory,
    NonPerformingAssetsCategoryMapAccounts,

    OtherAssetsScenario,
    OtherAssetsCategory,
    OtherAssets
)
from .request_post import others_assets_monthly_amount_clean
from .forms import (
    NonPerformingAssetsScenarioForm, ScenarioCloneForm, OthersAssetsScenarioForm,
    OtherAssetsDefineAmountMonthlyForm,
)
from .request_get import QueryGetParms
from utils.pagination import pagination
from utils.sql import execute_sql_query, execute_sql_query_no_return


@login_required()
@permission_required('ppto_maestro.puede_listar_nuevas_adquisiciones', raise_exception=True)
def scenarios_non_performing_assets(request):
    form = NonPerformingAssetsScenarioForm()

    def _sum_budgeted_by_category(created, qs_category):
        accounts_list = NonPerformingAssetsCategoryMapAccounts.objects.filter(
            category_id=qs_category.pk
        ).values_list('account_id', flat=True)
        qs_budgeted_for_scenario = BudgetedNonProductiveAssets.objects.filter(
            scenario_id=created.pk
        ).values_list('budgeted_asset_id', flat=True)

        qs = Detallexpresupuestoinversion.objects.extra({
            'presupuestado': 'SUM(Presupuestado)',
            'monto_depreciacion_anual': 'SUM(MontoDepreciacionAnual)',
        }).filter(
            pk__in=qs_budgeted_for_scenario,
            habilitado=True,
            codcentrocostoxcuentacontable__codcuentacontable__in=accounts_list
        ).values('presupuestado', 'monto_depreciacion_anual')
        monto_depreciacion_anual = qs[0].get('monto_depreciacion_anual', 0)
        presupuestado = qs[0].get('presupuestado', 0)
        return {
            'monto_depreciacion_anual': 0 if monto_depreciacion_anual is None else monto_depreciacion_anual, # NOQA
            'presupuestado': 0 if presupuestado is None else presupuestado
        }

    def _add_budgeted(qs_scenario, data):
        for investment in data:
            if not BudgetedNonProductiveAssets.objects.filter(
                scenario_id=qs_scenario.pk,
                budgeted_asset_id=investment.pk
            ).exists():
                BudgetedNonProductiveAssets.objects.create(
                    scenario_id=qs_scenario,
                    budgeted_asset_id=investment
                )

    def _correlative(period, total):
        return f'ESC-{period}-{total}'

    if request.method == "POST":
        if request.POST.get('method') == 'create':
            if not request.user.has_perm('ppto_maestro.puede_crear_escenarios_nuevas_adquisiciones'): # NOQA
                raise PermissionDenied
            form = NonPerformingAssetsScenarioForm(request.POST)
            if not form.is_valid():
                messages.warning(
                    request,
                    f'Formulario no v??lido: {form.errors.as_text()}'
                )
            else:
                if request.POST.get('is_active') == 'True':
                    NonPerformingAssetsScenario.objects.filter(
                        parameter_id=request.POST.get('parameter_id')
                    ).update(is_active=False)
                _new = form.save()
                _new.period_id = _new.parameter_id.period_id
                _new.created_by = request.user
                _new.updated_by = request.user
                _new.save()
                _new.correlative = _correlative(
                    _new.parameter_id.period_id.descperiodo,
                    NonPerformingAssetsScenario.objects.filter(
                        period_id=_new.period_id
                    ).count()
                )
                _new.save()
                messages.success(
                    request,
                    'Escenario creado con ??xito!'
                )
                qs_budgeted = Detallexpresupuestoinversion.objects.filter(
                    periodo=_new.period_id.pk,
                    habilitado=True,
                )
                _add_budgeted(_new, qs_budgeted)
                result = execute_sql_query(
                    (
                        f"EXEC [dbo].[sp_pptoMaestroBienesCapitalActivosFijosObtenerSaldoHist] " # NOQA
                        f"@ParametroId = {_new.parameter_id.pk}"
                    )
                )
                if result.get('status') == 'ok':
                    for category in result.get('data'):
                        qs_category = NonPerformingAssetsCategory.objects.filter(
                            identifier=category.get('CategoriaId')
                        ).first()
                        sum_category = _sum_budgeted_by_category(_new, qs_category)
                        NonPerformingAssetsXCategory.objects.create(
                            category_id=qs_category,
                            scenario_id=_new,
                            total_accumulated_balance=category.get('Saldo'),
                            accumulated_depreciation_balance=category.get('DepreciacionAcu'), # NOQA
                            depreciation_balance=category.get('Depreciacion'),
                            total_net_balance=category.get('ValorNeto'),
                            new_total_balance=sum_category.get('presupuestado', 0),
                            new_depreciation_balance=sum_category.get('monto_depreciacion_anual', 0) # NOQA
                        )
                else:
                    messages.danger(
                        request,
                        'No se pudo extraer informaci??n Historica'
                    )

                redirect_url = reverse(
                    'scenario_non_performing_assets', kwargs={'id': _new.pk}
                )
                full_redirect_url = f'{redirect_url}?option='
                return redirect(full_redirect_url)
        elif request.POST.get('method') == 'clone':
            if not request.user.has_perm('ppto_maestro.puede_editar_escenarios_nuevas_adquisiciones'):
                raise PermissionDenied
            id = request.POST.get('id')
            parameter_id = request.POST.get('parameter_id')
            comment = request.POST.get('comment')
            is_active = request.POST.get('is_active')
            qs_old_esc = get_object_or_404(NonPerformingAssetsScenario, pk=id)
            _clone = NonPerformingAssetsScenario.objects.get(pk=id)
            _clone.pk = None
            if not not parameter_id:
                qs_parameter = get_object_or_404(MasterParameters, pk=parameter_id)
                _clone.parameter_id = qs_parameter
                _clone.period_id = qs_parameter.period_id
            _clone.save()
            if is_active == 'True':
                NonPerformingAssetsScenario.objects.filter(
                    parameter_id=_clone.parameter_id.pk
                ).update(is_active=False)
            _clone.comment = comment
            _clone.is_active = is_active
            _clone.created_by = request.user
            _clone.updated_by = request.user
            _clone.correlative = _correlative(
                _clone.parameter_id.period_id.descperiodo,
                NonPerformingAssetsScenario.objects.filter(period_id=_clone.period_id).count()
            )
            _clone.save()
            _clone.refresh_from_db()
            messages.success(
                request, 'Escenario clonado con ??xito!'
            )

            qs_budgeted_for_scenario = BudgetedNonProductiveAssets.objects.filter(
                scenario_id=qs_old_esc.pk
            ).values_list('budgeted_asset_id', flat=True)
            qs_budgeted = Detallexpresupuestoinversion.objects.filter(
                pk__in=qs_budgeted_for_scenario
            )
            _add_budgeted(_clone, qs_budgeted)
            result = execute_sql_query(
                (
                    f"[dbo].[sp_pptoMaestroBienesCapitalActivosFijosObtenerSaldoHist] "
                    f"@ParametroId = {_clone.parameter_id.pk}"
                )
            )
            if result.get('status') == 'ok':
                for category in result.get('data'):
                    qs_category = NonPerformingAssetsCategory.objects.filter(
                        identifier=category.get('CategoriaId')
                    ).first()
                    old_category = NonPerformingAssetsXCategory.objects.filter(
                        scenario_id=qs_old_esc.pk, category_id=qs_category.pk
                    ).first()
                    sum_category = _sum_budgeted_by_category(_clone, qs_category)
                    NonPerformingAssetsXCategory.objects.create(
                        category_id=qs_category,
                        scenario_id=_clone,
                        total_accumulated_balance=category.get('Saldo'),
                        accumulated_depreciation_balance=category.get('DepreciacionAcu'), # NOQA
                        depreciation_balance=category.get('Depreciacion'),
                        total_net_balance=category.get('ValorNeto'),
                        new_total_balance=sum_category.get('presupuestado', 0),
                        new_depreciation_balance=sum_category.get('monto_depreciacion_anual', 0), # NOQA
                        comment_increases=old_category.comment_increases,
                        comment_decreases=old_category.comment_decreases,
                        amount_increases=old_category.amount_increases,
                        amount_decreases=old_category.amount_decreases
                    )
            else:
                messages.danger(
                    request,
                    'No se pudo extraer informaci??n Historica'
                )
            redirect_url = reverse(
                    'scenario_non_performing_assets', kwargs={'id': _clone.pk}
                )
            full_redirect_url = f'{redirect_url}?option='
            return redirect(full_redirect_url)
    query_parms = QueryGetParms(request.GET)
    filters = query_parms.get_query_filters()
    qs = NonPerformingAssetsScenario.objects.filter(**filters).exclude(deleted=True).order_by( # NOQA
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
    return render(request, 'non_performing_assets/scenarios.html', ctx)


@login_required()
@permission_required('ppto_maestro.puede_editar_escenarios_nuevas_adquisiciones', raise_exception=True) # NOQA
def scenario_non_performing_assets(request, id):
    qs = get_object_or_404(NonPerformingAssetsScenario, pk=id)

    if request.method == 'POST':
        if request.POST.get('method') == 'amount-increases-decreases':
            amount = request.POST.get('amount', '0').replace(',', '')
            row = get_object_or_404(NonPerformingAssetsXCategory, pk=request.POST.get('pk'))
            if request.POST.get('type') == 'decreases':
                row.amount_decreases = amount
                row.comment_decreases = request.POST.get('comment', 0)
                row.month_decreases = request.POST.get('month', 1)
                row.save()
            else:
                row.amount_increases = amount
                row.comment_increases = request.POST.get('comment', 0)
                row.month_increases = request.POST.get('month', 1)
                row.save()
            messages.success(request, 'Actualizaci??n realizada con ??xito!')
        elif request.POST.get('method') == 'edit-budgeted':
            remove = json.loads(request.POST.get('remove', '[]'))
            add = json.loads(request.POST.get('add', '[]'))
            if remove:
                for item in remove:
                    # Get record non-performining assets by Id from POST
                    qs_item = BudgetedNonProductiveAssets.objects.get(
                        budgeted_asset_id=item, scenario_id=qs.pk
                    )
                    amount = qs_item.budgeted_asset_id.presupuestado
                    depreciation = qs_item.budgeted_asset_id.monto_depreciacion_anual
                    account = qs_item.budgeted_asset_id.codcentrocostoxcuentacontable.codcuentacontable # NOQA

                    # GET by non-performining assets account the category in MAP model
                    category_account = NonPerformingAssetsCategoryMapAccounts.objects.filter( # NOQA
                        account_id=account.pk
                    ).first()

                    # Get category record and rest amount
                    # and total depreciation de non-performining assets
                    qs_category = NonPerformingAssetsXCategory.objects.get(
                        category_id=category_account.category_id, scenario_id=qs.pk
                    )
                    qs_category.new_depreciation_balance = qs_category.new_depreciation_balance - depreciation # NOQA
                    qs_category.new_total_balance = qs_category.new_total_balance - amount
                    qs_category.save()
                    qs_item.delete()
                messages.success(
                    request, f"Se han removido {len(remove)} activos del escenario con ??xito"
                )
            if add:
                for item in add:
                    qs_investment = Detallexpresupuestoinversion.objects.get(pk=item)

                    qs_item = BudgetedNonProductiveAssets()
                    qs_item.budgeted_asset_id = qs_investment
                    qs_item.scenario_id = qs
                    qs_item.save()

                    amount = qs_item.budgeted_asset_id.presupuestado
                    depreciation = qs_item.budgeted_asset_id.monto_depreciacion_anual
                    account = qs_item.budgeted_asset_id.codcentrocostoxcuentacontable.codcuentacontable # NOQA

                    category_account = NonPerformingAssetsCategoryMapAccounts.objects.filter( # NOQA
                        account_id=account.pk
                    ).first()

                    qs_category = NonPerformingAssetsXCategory.objects.get(
                        category_id=category_account.category_id, scenario_id=qs.pk
                    )
                    qs_category.new_depreciation_balance = qs_category.new_depreciation_balance + depreciation # NOQA
                    qs_category.new_total_balance = qs_category.new_total_balance + amount
                    qs_category.save()
                messages.success(
                    request, f"Se han agregado {len(add)} activos del escenario"
                )

        elif request.POST.get('method') == 'change-status':
            if not qs.is_active:
                NonPerformingAssetsScenario.objects.filter(
                    parameter_id=qs.parameter_id.pk
                ).update(is_active=False)
            qs.is_active = not qs.is_active
            qs.save()
            message = (
                f'Escenario actualizado a : '
                f'{"Principal" if qs.is_active else "Secundario"}'
                f' con ??xito!!'
            )
            messages.success(request, message)

        elif request.POST.get('method') == 'delete':
            qs.is_active = False
            qs.deleted = True
            qs.updated_by = request.user
            qs.save()
            messages.error(request, 'Escenario eliminado')
            return redirect('scenarios_non_performing_assets')
        elif request.POST.get('method') == 'update-cta':
            execute_sql_query_no_return(
                f"EXEC [dbo].[sp_pptoMaestroInversionesDepreciacionesMigrarPresupuestoIndirecto] "
                f"@CodPeriodo = {qs.period_id.pk} "
            )
            messages.success(request, 'Actualizaci??n realizada con ??xito!')

    qs_details = NonPerformingAssetsXCategory.objects.filter(
        scenario_id=qs.pk
    ).order_by('category_id')
    qs_sum = NonPerformingAssetsXCategory.objects.filter(scenario_id=qs.pk).extra({
        'sum_saldo_total_acumulado': 'SUM(SaldoTotalAcumulado)',
        'sum_saldo_depreciacion_acumulado': 'SUM(SaldoDepreciacionAcumulado)',
        'sum_depreciacion': 'SUM(SaldoDepreciacion)',
        'sum_total_neto': 'SUM(SaldoTotalNeto)',
        'sum_monto_aumento': 'SUM(MontoAumento)',
        'sum_disminucion': 'SUM(MontoDisminucion)',
        'sum_nuevo_saldo': 'SUM(NuevoSaldoTotal)',
        'sum_nueva_depreciacion': 'SUM(NuevoSaldoDepreciacion)',
    }).values(
        'sum_saldo_total_acumulado', 'sum_saldo_depreciacion_acumulado',
        'sum_depreciacion', 'sum_total_neto',
        'sum_monto_aumento', 'sum_disminucion',
        'sum_nuevo_saldo', 'sum_nueva_depreciacion'
    )

    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')
    qs_budgeted_for_scenario = BudgetedNonProductiveAssets.objects.filter(
        scenario_id=qs.pk
    ).values_list('budgeted_asset_id', flat=True)
    qs_budgeted = Detallexpresupuestoinversion.objects.filter(
        habilitado=True, periodo=qs.period_id.pk
    ).filter(
        Q(descproducto__icontains=q) |
        Q(codcentrocostoxcuentacontable__codcentrocosto__desccentrocosto__icontains=q) |
        Q(codcentrocostoxcuentacontable__codcuentacontable__desccuentacontable__icontains=q) | # NOQA
        Q(presupuestado__icontains=q)
    ).order_by('-presupuestado')
    result = pagination(qs=qs_budgeted, page=page, page_size=40)
    global_non_performing_assets = scenario_global_non_performing_assets(
        qs.parameter_id.pk
    )
    ctx = {
        'qs': qs,
        'qs_details': qs_details,
        'global_non_performing_assets': global_non_performing_assets,
        'qs_budgeted_for_scenario': qs_budgeted_for_scenario,
        'qs_sum': qs_sum[0],
        'result': result,
        'months': MONTH_CHOICES,
        'form_clone': ScenarioCloneForm()
    }
    return render(request, 'non_performing_assets/scenario.html', ctx)


@login_required()
@permission_required('ppto_maestro.puede_listar_escenarios_otros_activos', raise_exception=True)
def scenarios_others_assets(request):
    form = OthersAssetsScenarioForm()

    def _correlative(period, total):
        return f'ESC-{period}-{total}'

    if request.POST:
        if request.POST.get('method') == 'create':
            if not request.user.has_perm('ppto_maestro.puede_crear_escenarios_otros_activos'):
                raise PermissionDenied
            form = OthersAssetsScenarioForm(request.POST)
            if not form.is_valid():
                messages.warning(request, f'Formulario no v??lido: {form.errors.as_text()}')
            else:
                if request.POST.get('is_active') == 'True':
                    OtherAssetsScenario.objects.filter(
                        parameter_id=request.POST.get('parameter_id')
                    ).update(is_active=False)
                _new = form.save()
                _new.period_id = _new.parameter_id.period_id
                _new.created_by = request.user
                _new.updated_by = request.user
                _new.save()
                _new.correlative = _correlative(
                    _new.parameter_id.period_id.descperiodo,
                    OtherAssetsScenario.objects.filter(
                        period_id=_new.period_id
                    ).count()
                )
                _new.save()
                messages.success(request, 'Escenario creado con ??xito!')
                for qs_category in OtherAssetsCategory.objects.filter(is_active=True):
                    query = f"{qs_category.identifier} '{_new.parameter_id.pk}'"
                    result = execute_sql_query(query)
                    if result.get('status') == 'ok':
                        for item in result.get('data'):
                            OtherAssets.objects.create(
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
                            request, f'No se pudo extraer informaci??n Historica de categoria: {qs_category}' # NOQA
                        )
                redirect_url = reverse('scenario_others_assets', kwargs={'id': _new.pk})
                full_redirect_url = f'{redirect_url}?option='
                return redirect(full_redirect_url)
        elif request.POST.get('method') == 'clone':
            if not request.user.has_perm('ppto_maestro.puede_editar_escenarios_otros_activos'):
                raise PermissionDenied
            id = request.POST.get('id')
            comment = request.POST.get('comment')
            is_active = request.POST.get('is_active')
            qs_old_esc = get_object_or_404(OtherAssetsScenario, pk=id)
            _clone = OtherAssetsScenario.objects.get(pk=id)
            _clone.pk = None
            _clone.save()
            if is_active == 'True':
                OtherAssetsScenario.objects.filter(
                    parameter_id=_clone.parameter_id.pk
                ).update(is_active=False)
            _clone.comment = comment
            _clone.is_active = is_active
            _clone.created_by = request.user
            _clone.updated_by = request.user
            _clone.correlative = _correlative(
                _clone.parameter_id.period_id.descperiodo,
                OtherAssetsScenario.objects.filter(
                    period_id=_clone.period_id
                ).count()
            )
            _clone.save()
            _clone.refresh_from_db()
            for item_category in OtherAssets.objects.filter(scenario_id=qs_old_esc.pk):
                _new = OtherAssets.objects.get(pk=item_category.pk)
                _new.pk = None
                _new.save()
                _new.scenario_id = _clone
                _new.save()
            messages.success(request, 'Escenario clonado con ??xito!')
            redirect_url = reverse(
                'scenario_others_assets', kwargs={'id': _clone.pk}
            )
            full_redirect_url = f'{redirect_url}?option='
            return redirect(full_redirect_url)

    query_parms = QueryGetParms(request.GET)
    filters = query_parms.get_query_filters()
    qs = OtherAssetsScenario.objects.filter(**filters).exclude(deleted=True).order_by(
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
    return render(request, 'others_assets/scenarios.html', ctx)


@login_required()
@permission_required('ppto_maestro.puede_editar_escenarios_otros_activos', raise_exception=True)
def scenario_others_assets(request, id):
    qs = get_object_or_404(OtherAssetsScenario, pk=id)
    qs_categories = OtherAssetsCategory.objects.all().order_by('name')
    qs_details = OtherAssets.objects.filter(scenario_id=qs.pk).order_by(
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
            item = get_object_or_404(OtherAssets, pk=request.POST.get('pk'))
            item.comment = request.POST.get('comment', '')
            item.percentage = request.POST.get('percentage').replace(',', '')
            item.new_balance = request.POST.get('new_balance').replace(',', '')
            item.criteria = request.POST.get('criteria')
            item.save()
            messages.success(request, "Actualizaci??n realizada con ??xito!")
        elif request.POST.get('method') == 'define-monthly-by-amount':
            qs_item = get_object_or_404(OtherAssets, pk=request.POST.get('pk'))
            data = others_assets_monthly_amount_clean(request.POST)
            form = OtherAssetsDefineAmountMonthlyForm(data, instance=qs_item)
            if not form.is_valid():
                messages.warning(request, f'Formulario no v??lido: {form.errors.as_text()}')
            else:
                OtherAssets.objects.filter(pk=qs_item.pk).update(**form.cleaned_data)
                messages.success(request, "Actualizaci??n realizada con ??xito!")
        elif request.POST.get('method') == 'change-status':
            if not qs.is_active:
                OtherAssetsScenario.objects.filter(
                    parameter_id=qs.parameter_id.pk
                ).update(is_active=False)
            qs.is_active = not qs.is_active
            qs.save()
            message = (
                f'Escenario actualizado a : '
                f'{"Principal" if qs.is_active else "Secundario"}'
                f' con ??xito!!'
            )
            messages.success(request, message)
        elif request.POST.get('method') == 'delete':
            qs.is_active = False
            qs.deleted = True
            qs.updated_by = request.user
            qs.save()
            messages.error(request, 'Escenario eliminado')
            return redirect('scenarios_others_assets')

    global_non_performing_assets = scenario_global_non_performing_assets(
        qs.parameter_id.pk
    )
    ctx = {
        'qs': qs,
        'global_non_performing_assets': global_non_performing_assets,
        'qs_details': _struct_data_by_order(),
        'others_assets_criteria': OTHERS_ASSETS_CRITERIA,
        'form_clone': ScenarioCloneForm()
    }
    return render(request, 'others_assets/scenario.html', ctx)


def scenario_global_non_performing_assets(parameter_id):

    def _new_total_net_balance(data):
        total_subtract = (
            data.get('sum_depreciacion', 0) +
            data.get('sum_disminucion', 0) +
            data.get('sum_nueva_depreciacion', 0)
        )
        total_add = (
            data.get('sum_total_neto', 0) +
            data.get('sum_monto_aumento', 0) +
            data.get('sum_nuevo_saldo', 0)
        )
        return total_add - total_subtract

    global_non_performing_assets = []
    non_performing_assets_scenario = NonPerformingAssetsScenario.objects.filter(
        parameter_id=parameter_id, is_active=True
    ).first()
    non_others_assets_scenario = OtherAssetsScenario.objects.filter(
        parameter_id=parameter_id, is_active=True
    ).first()

    if non_performing_assets_scenario:
        non_performing_assets = NonPerformingAssetsXCategory.objects.filter(
            scenario_id=non_performing_assets_scenario.pk
        ).extra({
            'sum_saldo_total_acumulado': 'SUM(SaldoTotalAcumulado)',
            'sum_saldo_depreciacion_acumulado': 'SUM(SaldoDepreciacionAcumulado)',
            'sum_depreciacion': 'SUM(SaldoDepreciacion)',
            'sum_total_neto': 'SUM(SaldoTotalNeto)',
            'sum_monto_aumento': 'SUM(MontoAumento)',
            'sum_disminucion': 'SUM(MontoDisminucion)',
            'sum_nuevo_saldo': 'SUM(NuevoSaldoTotal)',
            'sum_nueva_depreciacion': 'SUM(NuevoSaldoDepreciacion)',
        }).values(
            'sum_saldo_total_acumulado', 'sum_saldo_depreciacion_acumulado',
            'sum_depreciacion', 'sum_total_neto',
            'sum_monto_aumento', 'sum_disminucion',
            'sum_nuevo_saldo', 'sum_nueva_depreciacion'
        )
        non_performing_assets = non_performing_assets[0]

        global_non_performing_assets.append({
            'name': 'Activos Fijos Netos',
            'previous_total_net_balance': non_performing_assets.get('sum_total_neto', 0),
            'new_total_net_balance': _new_total_net_balance(non_performing_assets)
        })

    if non_others_assets_scenario:
        others_assets = OtherAssets.objects.values('category_id__name').filter(
            scenario_id=non_others_assets_scenario.pk
        ).order_by('category_id').annotate(
            total_previous=Sum('previous_balance'),
            total_budgeted=Sum('new_balance')
        )
        for other_assets in others_assets:
            global_non_performing_assets.append({
                'name': other_assets.get('category_id__name'),
                'previous_total_net_balance': other_assets.get('total_previous'),
                'new_total_net_balance': other_assets.get('total_budgeted')
            })

    return global_non_performing_assets
