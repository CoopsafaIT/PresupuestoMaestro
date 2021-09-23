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

from ppto_safa.constants import STAFF_POSITIONS, MONTHS_LIST
from apps.main.models import (
    Centroscosto,
    Detallexpresupuestopersonal,
    Periodo,
    Puestos,
)
from apps.staff_budgets.reports import create_excel_report
from apps.staff_budgets.forms import StaffCUForm


@login_required()
def staff_budgets_register(request):
    if request.method == 'POST':
        if request.POST.get('method') == 'filter-staff-budget':
            request.session['period'] = request.POST.get('period', '')
            request.session['cost_center'] = request.POST.get('cost_center', '')

        elif request.POST.get('method') == 'create-staff-budget':
            try:
                request.session['period'] = request.POST.get('period', '')
                request.session['cost_center'] = request.POST.get('cost_center', '')
                form = StaffCUForm(request.POST)
                if not form.is_valid():
                    raise ValidationError(f'{ form.errors.as_text() }')

                job_position = Puestos.objects.get(
                    pk=form.cleaned_data.get('job_position')
                )
                cost_center = Centroscosto.objects.get(
                    pk=form.cleaned_data.get('cost_center')
                )
                period = Periodo.objects.get(pk=form.cleaned_data.get('period'))
                new_record = Detallexpresupuestopersonal()
                new_record.periodo = period
                new_record.codpuesto = job_position
                new_record.codcentrocosto = cost_center
                new_record.mes = form.cleaned_data.get('month')
                new_record.cantidad = form.cleaned_data.get('number')
                new_record.disponible = form.cleaned_data.get('number')
                new_record.sueldo = 0
                new_record.tipo = form.cleaned_data.get('type_position')
                new_record.mesfin = form.cleaned_data.get('month_end')
                new_record.justificacion = form.cleaned_data.get('justification')
                new_record.usuariocreacion = request.user
                new_record.fechacreacion = dt.datetime.today()
                new_record.save()
                messages.success(
                    request,
                    'Personal registrado con éxito!'
                )
            except (
                Centroscosto.DoesNotExist,
                Puestos.DoesNotExist,
                Periodo.DoesNotExist
            ) as e:
                messages.warning(
                    request,
                    f'No encontrado: {e.__str__()}'
                )
                return redirect('staff_budgets_register')
            except ValidationError as e:
                messages.warning(
                    request,
                    f'Error de validacion de formulario: {e.__str__()}'
                )
                return redirect('staff_budgets_register')
            except Exception as e:
                messages.error(
                    request,
                    f'Exception no determinada: {e.__str__()}'
                )
                return redirect('staff_budgets_register')

    periods = Periodo.objects.filter(habilitado=True)
    cost_centers = Centroscosto.objects.filter(habilitado=True)
    job_positions = Puestos.objects.filter(puestoestado=True)
    ctx = {
        'periods': periods,
        'cost_centers': cost_centers,
        'job_positions': job_positions,
        'staff_positions': STAFF_POSITIONS,
        'months': MONTHS_LIST,
    }
    if (
        request.session.get('period', None) and
        request.session.get('cost_center', None)
    ):
        qs = Detallexpresupuestopersonal.objects.filter(
            codcentrocosto=request.session.get('cost_center'),
            periodo=request.session.get('period')
        )
        ctx['qs'] = qs
    return render(request, 'staff_budgets_register.html', ctx)


@login_required()
def staff_budgets_update(request, id):
    if request.method == 'POST':
        try:
            request.session['period'] = request.POST.get('period', '')
            request.session['cost_center'] = request.POST.get('cost_center', '')
            form = StaffCUForm(request.POST)
            if not form.is_valid():
                raise ValidationError(f'{ form.errors.as_text() }')

            job_position = Puestos.objects.get(
                pk=form.cleaned_data.get('job_position')
            )
            cost_center = Centroscosto.objects.get(
                pk=form.cleaned_data.get('cost_center')
            )
            period = Periodo.objects.get(pk=form.cleaned_data.get('period'))
            upd_record = Detallexpresupuestopersonal.objects.get(pk=id)
            upd_record.periodo = period
            upd_record.codpuesto = job_position
            upd_record.codcentrocosto = cost_center
            upd_record.mes = form.cleaned_data.get('month')
            upd_record.cantidad = form.cleaned_data.get('number')
            upd_record.disponible = form.cleaned_data.get('number')
            upd_record.sueldo = 0
            upd_record.tipo = form.cleaned_data.get('type_position')
            upd_record.mesfin = form.cleaned_data.get('month_end')
            upd_record.justificacion = form.cleaned_data.get('justification')
            upd_record.save()
            messages.success(
                request,
                'Presupuesto de personal editado con éxito!'
            )
            return redirect('staff_budgets_register')
        except (
            Centroscosto.DoesNotExist,
            Puestos.DoesNotExist,
            Periodo.DoesNotExist,
            Detallexpresupuestopersonal.DoesNotExist
        ) as e:
            messages.warning(
                request,
                f'No encontrado: {e.__str__()}'
            )
            return redirect(reverse('staff_budgets_update', kwargs={'id': id}))
        except ValidationError as e:
            messages.warning(
                request,
                f'Error de validacion de formulario: {e.__str__()}'
            )
            return redirect(reverse('staff_budgets_update', kwargs={'id': id}))
        except Exception as e:
            messages.error(
                request,
                f'Exception no determinada: {e.__str__()}'
            )
            return redirect(reverse('staff_budgets_update', kwargs={'id': id}))       
    else:
        qs = get_object_or_404(Detallexpresupuestopersonal, pk=id)
        periods = Periodo.objects.filter(habilitado=True)
        cost_centers = Centroscosto.objects.filter(habilitado=True)
        job_positions = Puestos.objects.filter(puestoestado=True)
        ctx = {
            'qs': qs,
            'periods': periods,
            'cost_centers': cost_centers,
            'job_positions': job_positions,
            'staff_positions': STAFF_POSITIONS,
            'months': MONTHS_LIST,
        }
        return render(request, 'staff_budgets_update.html', ctx)


@login_required()
def staff_budgets_delete(request, id):
    if request.method == 'POST':
        try:
            Detallexpresupuestopersonal.objects.filter(pk=id).delete()
            messages.success(
                request,
                'Presupuesto de personal eliminado con éxito'
            )
        except Exception as e:
            messages.error(
                request,
                f'No se pudo eliminar {e.__str__()}'
            )
        return redirect('staff_budgets_register')


@login_required()
def generate_excel_report(request, period, cost_center):
    qs = Detallexpresupuestopersonal.objects.values(
        'tipo',
        'mes',
        'cantidad',
        'mesfin',
        'justificacion',
        'codpuesto__descpuesto',
        'codcentrocosto__desccentrocosto',
        'periodo__descperiodo'
    ).filter(
        codcentrocosto=cost_center,
        periodo=period
    ).order_by('tipo')
    return create_excel_report(qs)
