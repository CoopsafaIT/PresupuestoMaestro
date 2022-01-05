import datetime as dt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from apps.main.models import (
    Criterios,
    Centroscosto,
    Cuentascontables,
    Inversiones,
    Puestos,
    Proyectos,
    Periodo,
    Tiposcuenta,

)
from apps.administration.forms import (
    CuentascontablesForm,
    InversionesForm,
    PuestosForm,
    ProjectionForm,
)
from utils.pagination import pagination
from utils.constants import PROJECTION_SP
from utils.sql import execute_sql_query, execute_sql_query_no_return


@login_required
@permission_required(
    'admin.puede_listar_centros_costos', raise_exception=True
)
def cost_centers(request):
    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')
    qs = Centroscosto.objects.filter(
        Q(desccentrocosto__icontains=q) | Q(codigocentrocosto__icontains=q)
    )
    result = pagination(qs=qs, page=page)
    ctx = {
        'qs': result,
    }
    return render(request, 'cost_centers/cost_centers.html', ctx)


@login_required
@permission_required(
    'admin.puede_listar_cuentas_inversion', raise_exception=True
)
def investment_accounts(request):
    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')
    form = CuentascontablesForm()
    if request.method == 'POST':
        if not request.user.has_perm('admin.puede_ingresar_cuentas_inversion'):
            raise PermissionDenied
        form = CuentascontablesForm(request.POST)
        if not form.is_valid():
            messages.warning(
                request,
                f'Formulario no válido, por favor revisar. {form.errors.as_text()}'
            )
        else:
            instance = form.save()
            last_record = Cuentascontables.objects.filter(codtipocuenta=2).count()
            instance.codtipocuenta = Tiposcuenta.objects.get(pk=2)
            instance.desccuentacontable = instance.desccuentacontable.upper()
            instance.codigocuentacontable = int(last_record) + 1
            instance.fechacreacion = dt.datetime.now()
            instance.usuariocreacion = request.user
            instance.fechamodificacion = dt.datetime.now()
            instance.usuariomodificacion = request.user.pk
            instance.save()
            messages.success(
                request,
                f'Cuenta Contable: {instance.desccuentacontable} creada con éxito'
            )

    qs = Cuentascontables.objects.filter(
        Q(codigocuentacontable__icontains=q) | Q(desccuentacontable__icontains=q)
    ).filter(codtipocuenta=2)
    result = pagination(qs=qs, page=page)
    ctx = {
        'qs': result,
        'form': form,
    }
    return render(request, 'investment_accounts/list.html', ctx)


@login_required
@permission_required(
    'admin.puede_editar_cuentas_inversion', raise_exception=True
)
def investment_account(request, id):
    qs = get_object_or_404(Cuentascontables, pk=id)
    form = CuentascontablesForm(instance=qs)
    if request.method == 'POST':
        form = CuentascontablesForm(request.POST, instance=qs)
        if not form.is_valid():
            messages.warning(
                request,
                f'Formulario no válido, por favor revisar. {form.errors.as_text()}'
            )
        else:
            instance = form.save()
            instance.desccuentacontable = instance.desccuentacontable.upper()
            instance.fechamodificacion = dt.datetime.now()
            instance.usuariomodificacion = request.user.pk
            instance.save()
            messages.success(
                request,
                f'Cuenta Contable: {instance.desccuentacontable} editada con éxito'
            )
            return redirect('investment_accounts')
    ctx = {
        'qs': qs,
        'form': form,
    }
    return render(request, 'investment_accounts/edit.html', ctx)


@login_required
@permission_required(
    'admin.puede_listar_inversiones', raise_exception=True
)
def investments(request):
    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')
    form = InversionesForm()
    if request.method == 'POST':
        if not request.user.has_perm('admin.puede_ingresar_inversiones'):
            raise PermissionDenied
        form = InversionesForm(request.POST)
        if not form.is_valid():
            messages.warning(
                request,
                f'Formulario no válido, por favor revisar. {form.errors.as_text()}'
            )
        else:
            instance = form.save()
            instance.fechacreacion = dt.datetime.now()
            instance.usuariocreacion = request.user.pk
            instance.fechamodificacion = dt.datetime.now()
            instance.usuariomodificacion = request.user.pk
            instance.save()
            messages.success(
                request,
                f'Inversión: {instance.descinversion} creada con éxito'
            )
    qs = Inversiones.objects.filter(
        Q(codcuentacontable__desccuentacontable__icontains=q) |
        Q(descinversion__icontains=q)
    )

    result = pagination(qs=qs, page=page)
    ctx = {
        'qs': result,
        'form': form
    }
    return render(request, 'investment/list.html', ctx)


@login_required
@permission_required(
    'admin.puede_editar_inversiones', raise_exception=True
)
def investment(request, id):
    qs = get_object_or_404(Inversiones, pk=id)
    form = InversionesForm(instance=qs)
    if request.method == 'POST':
        form = InversionesForm(request.POST, instance=qs)
        if not form.is_valid():
            messages.warning(
                request,
                f'Formulario no válido, por favor revisar. {form.errors.as_text()}'
            )
        else:
            instance = form.save()
            instance.fechamodificacion = dt.datetime.now()
            instance.usuariomodificacion = request.user.pk
            instance.save()
            messages.success(
                request,
                f'Inversión: {instance.descinversion} creada con éxito'
            )
            return redirect('investments')
    ctx = {
        'qs': qs,
        'form': form,
    }
    return render(request, 'investment/edit.html', ctx)


@login_required
@permission_required(
    'admin.puede_editar_indice_inflacionario', raise_exception=True
)
def inflationary_index(request):
    qs = get_object_or_404(Criterios, pk=1)
    if request.method == 'POST':
        qs.valor = request.POST.get('value')
        qs.save()
        messages.success(
            request,
            'Indice Inflacionario Editado con éxito!'
        )
    ctx = {
        'qs': qs
    }
    return render(request, 'inflationary_index.html', ctx)


@login_required
@permission_required(
    'admin.puede_listar_puestos_trabajo', raise_exception=True
)
def job_positions(request):
    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')
    form = PuestosForm()
    if request.method == 'POST':
        if not request.user.has_perm('admin.puede_crear_puestos_trabajo'):
            raise PermissionDenied
        form = PuestosForm(request.POST)
        if not form.is_valid():
            messages.warning(
                request,
                f'Formulario no válido, por favor revisar. {form.errors.as_text()}'
            )
        else:
            instance = form.save()
            instance.descpuesto = instance.descpuesto.upper()
            instance.save()
            messages.success(
                request,
                f'Puesto de trabajo: {instance.descpuesto} creado con éxito'
            )

    qs = Puestos.objects.filter(
        Q(descpuesto__icontains=q) |
        Q(sueldopermanente__icontains=q) |
        Q(sueldotemporal__icontains=q)
    )

    result = pagination(qs=qs, page=page)
    ctx = {
        'qs': result,
        'form': form
    }
    return render(request, 'job_positions/list.html', ctx)


@login_required
@permission_required(
    'admin.puede_editar_puestos_trabajo', raise_exception=True
)
def job_position(request, id):
    qs = get_object_or_404(Puestos, pk=id)
    form = PuestosForm(instance=qs)
    if request.method == 'POST':
        form = PuestosForm(request.POST, instance=qs)
        if not form.is_valid():
            messages.warning(
                request,
                f'Formulario no válido, por favor revisar. {form.errors.as_text()}'
            )
        else:
            instance = form.save()
            instance.descpuesto = instance.descpuesto.upper()
            instance.save()
            messages.success(
                request,
                f'Puesto de trabajo: {instance.descpuesto} editado con éxito'
            )
            return redirect('job_positions')
    ctx = {
        'qs': qs,
        'form': form,
    }
    return render(request, 'investment/edit.html', ctx)


@login_required
@permission_required(
    'admin.puede_ingresar_proyeccion', raise_exception=True
)
def projections(request):
    form = ProjectionForm()
    if request.method == 'POST':
        form = ProjectionForm(request.POST)
        if form.is_valid():
            period = request.POST.get('period')
            year_base = request.POST.get('year_base')
            month_base = request.POST.get('month_base')
            sp_name = dict(PROJECTION_SP).get(request.POST.get('projection_type'))
            query = f'EXEC {sp_name}@Periodo={period}, @Ano={year_base}, @Mes={month_base}'
            execute_sql_query(query)
            messages.success(request, 'Proyección Ingresada con éxito!')
    ctx = {
        'form': form
    }
    return render(request, 'projections.html', ctx)


@login_required
@permission_required(
    'admin.puede_listar_proyectos', raise_exception=True
)
def projects(request):
    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')
    qs = Proyectos.objects.filter(
        Q(descproyecto__icontains=q) |
        Q(codcentrocosto__desccentrocosto__icontains=q)
    )

    result = pagination(qs=qs, page=page)
    ctx = {
        'qs': result,
    }
    return render(request, 'projects/list.html', ctx)


@login_required
def periods(request):
    page = request.GET.get('page', 1)
    q = request.GET.get('q', '')

    if request.method == 'POST':
        last = Periodo.objects.all().order_by(
            'descperiodo'
        ).last().descperiodo
        period = Periodo()
        period.descperiodo = int(last) + 1
        period.usuariocreacion = request.user
        period.habilitado = True
        period.cerrado = False
        period.save()
        messages.success(
            request,
            f'Periodo: {period.descperiodo} creado con éxito'
        )

    qs = Periodo.objects.filter(
        Q(descperiodo__icontains=q) |
        Q(fechalimite__icontains=q)
    )
    result = pagination(qs=qs, page=page)
    ctx = {
        'qs': result,
    }
    return render(request, 'periods/list.html', ctx)


@login_required
@permission_required(
    'admin.puede_editar_periodos', raise_exception=True
)
def period(request, id):
    if request.method == 'POST':
        qs = get_object_or_404(Periodo, pk=id)
        if request.POST.get('method') == 'close':
            qs.cerrado = True
            qs.save()
            messages.success(
                request,
                f'Periodo: {qs.descperiodo} cerrado con éxito'
            )
        elif request.POST.get('method') == 'change-status':
            qs.habilitado = not qs.habilitado
            qs.save()
            status = 'Activo' if qs.habilitado else 'Inactivo'
            message = (
                f'Periodo: {qs.descperiodo} '
                f'cambiado a estado  {status} con éxito'
            )
            messages.success(
                request,
                message
            )
        return redirect('periods')


@login_required
@permission_required(
    'admin.puede_listar_control_ppto_centros_costos', raise_exception=True
)
def control_budgeted_cost_centers(request):
    if request.method == 'GET':
        request.session['period'] = request.GET.get('period')
    periods = Periodo.objects.all()
    ctx = {
        'periods': periods
    }

    if request.session.get('period'):
        period = request.session.get('period')
        page = request.GET.get('page', 1)
        query = (
            f"SELECT SUM(CASE WHEN Estado=1 THEN 1 ELSE 0 END) as Presupuestada, "
            f"COUNT(*) as Totales,CC.DescCentroCosto,PR.DescProyecto,CC.CodCentroCosto "
            f"FROM [PresupuestoSafa].[dbo].[Presupuestos] A INNER JOIN "
            f"PresupuestoSafa.dbo.Periodo B on A.CodPeriodo = B.CodPeriodo INNER JOIN "
            f"PresupuestoSafa.dbo.CentroCostoXCuentaContable  C on "
            f"A.CodCentrosCostoXCuentaContable = C.CodCentroCostoXCuentaContable "
            f"inner join PresupuestoSafa.dbo.Proyectos PR on PR.CodProyecto = "
            f"A.CodProyecto INNER JOIN PresupuestoSafa.dbo.CentrosCosto CC on "
            f"C.CodCentroCosto = cc.CodCentroCosto Where  CodTipoPresupuesto=1 and "
            f"A.CodPeriodo = {period} and C.Habilitado=1 "
            f"group by cc.DescCentroCosto,PR.DescProyecto ,CC.CodCentroCosto "
            f"order by DescCentroCosto"
        )
        result = execute_sql_query(query)
        if result.get('status') == 'ok':
            for item in result.get('data'):
                item['Diferencia'] = item.get('Totales') - item.get('Presupuestada')
            ctx['data'] = pagination(qs=result.get('data'), page=page)

    return render(request, 'control_budgeted_cost_centers.html', ctx)


@login_required
@permission_required(
    'admin.puede_inicializar_ppto', raise_exception=True
)
def budget_init(request):
    if request.method == 'POST':
        period = get_object_or_404(Periodo, pk=request.POST.get('period'))
        query = f"EXEC [dbo].[InicializarPresupuestos] @Periodo = '{period.descperiodo}'"
        result = execute_sql_query_no_return(query)
        if result.get('status') == 'ok':
            messages.success(
                request,
                'Inicialización de Presupuestos realizado con éxito'
            )
        else:
            messages.warning(
                request,
                f'No se pudo realizar inicialización: {result.get("data","")}'
            )
    periods = Periodo.objects.filter(habilitado=True, cerrado=False)
    ctx = {
        'periods': periods
    }
    return render(request, 'budget_init.html', ctx)
