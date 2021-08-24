import datetime as dt

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from apps.main.models import (
    Centroscosto,
    Detallexpresupuestoviaticos,
    Filiales,
    Periodo,
)
from apps.travel_budgets.forms import (
    InternacionalTravelBudget,
    NacionalTravelBudget
)
from ppto_safa.constants import TRAVEL_CATEGORY, ZONES
from apps.travel_budgets.reports import create_excel_report


@login_required()
def travel_budget_register(request):
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
                cost_centers = Centroscosto.objects.filter(habilitado=True)
                filials = Filiales.objects.all()
                ctx = {
                    'periods': periods,
                    'cost_centers': cost_centers,
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
                        'Presupuesto para viatico internacional registrado con éxito'
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
                cost_centers = Centroscosto.objects.filter(habilitado=True)
                filials = Filiales.objects.all()
                ctx = {
                    'periods': periods,
                    'cost_centers': cost_centers,
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
                        'Presupuesto para viatico nacional registrado con éxito'
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
                cost_centers = Centroscosto.objects.filter(habilitado=True)
                filials = Filiales.objects.all()
                ctx = {
                    'periods': periods,
                    'cost_centers': cost_centers,
                    'filials': filials,
                    'categories': TRAVEL_CATEGORY,
                    'zones': ZONES,
                    'qs_international_travel_budget': qs_international_travel_budget,
                    'qs_national_travel_budget': qs_national_travel_budget
                }
                return render(request, 'travel_budget_register.html', ctx)

    else:
        periods = Periodo.objects.filter(habilitado=True)
        cost_centers = Centroscosto.objects.filter(habilitado=True)
        filials = Filiales.objects.all()
        ctx = {
            'periods': periods,
            'cost_centers': cost_centers,
            'filials': filials,
            'categories': TRAVEL_CATEGORY,
            'zones': ZONES
        }
        if (
            request.session.get('period', None) and
            request.session.get('cost_center', None)
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
                    'Presupuesto para viatico internacional editado con éxito'
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
                    'Presupuesto para viatico nacional registrado con éxito'
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
            'Presupuesto de viatico eliminado con éxito'
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
