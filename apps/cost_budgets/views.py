import datetime as dt

from decimal import Decimal as dc
from django.shortcuts import (
    render,
    redirect,
)
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Sum, F
from openpyxl.utils.exceptions import InvalidFileException

from apps.main.models import (
    Periodo,
    Presupuestocostos,
)
from ppto_safa.utils import (
    execute_sql_query,
    try_convert_float
)
from utils.constants import MONTH
from apps.cost_budgets.reports import (
    generate_excel_file_format,
    load_excel_file
)


@login_required()
@permission_required(
    'ppto_costos.puede_ingresar_ppto_costos', raise_exception=True
)
def cost_budget_register(request):
    if request.method == 'POST':
        if request.POST.get('method') == 'load-excel-file':
            try:
                result = load_excel_file(request.FILES['excel-file'])
                sheet = result.get('sheet')
                number_rows = result.get('number_rows')
                counter = 2
                for item in range(1, number_rows):
                    period = Periodo.objects.get(descperiodo=sheet[f'E{counter}'].value)
                    if sheet[f'D{counter}'].value is None:
                        value = 0
                    else:
                        value = float(sheet[f'D{counter}'].value)

                    upd_record = Presupuestocostos.objects.get(
                        codcentrocostoxcuentacontable_new=sheet[f'A{counter}'].value,
                        periodo=period.pk
                    )
                    upd_record.valor = value
                    upd_record.total = value
                    upd_record.fechamodificacion = dt.datetime.today()
                    upd_record.usuariomodificacion = request.user
                    upd_record.save()
                    counter = counter + 1

                msg = (
                    f'Archivo cargado con exito! '
                    f'Numero de lineas leidas : {counter - 1 }'
                )
                messages.success(request, msg)
            except InvalidFileException as e:
                messages.warning(
                    request,
                    f'Archivo de excel: {e.__str__()}'
                )
                return redirect('indirect_budget_register')
            except Presupuestocostos.DoesNotExist as e:
                messages.warning(
                    request,
                    f'No encontrado: {e.__str__()}'
                )
                return redirect('indirect_budget_register')
            except Exception as e:
                messages.error(
                    request,
                    f'Execption catched: {e.__str__() }'
                )
                return redirect('indirect_budget_register')

        if request.POST.get('method') == 'recalculate':
            try:
                request.session['period'] = request.POST.get('period')
                request.session['account'] = request.POST.get('account')
                account = request.POST.get('account')
                period = request.POST.get('period')
                values = request.POST.getlist('value[]', [])
                ids = request.POST.getlist('id[]', [])
                qs = Presupuestocostos.objects.filter(
                    pk__in=ids
                ).order_by('-pk')
                list_items_to_update = []
                for key, val in enumerate(qs):
                    value = values[key].replace(',', '')
                    result = try_convert_float(value)
                    if type(result).__name__ == 'str':
                        result = 0
                        messages.warning(
                            request,
                            f'Valor ({values[key]}) del Centro de costos: '
                            f'{val.codcentrocostoxcuentacontable_new.codcentrocosto} '
                            f'no es un valor valido!'
                        )
                    if val.total != result:
                        list_items_to_update.append({
                            'id': val.pk,
                            'value': result
                        })
                for item in list_items_to_update:
                    Presupuestocostos.objects.filter(
                        pk=item.get('id')
                    ).update(
                        total=item.get('value'),
                        valor=item.get('value')
                    )

                total = dict(Presupuestocostos.objects.filter(
                    codcentrocostoxcuentacontable_new__codcuentacontable__cuentapadre=account, # NOQA
                    periodo=period
                ).aggregate(
                    total_ejecutado_diciembre=Sum('ejecutadodiciembre'),
                    porcentaje=Sum('porcentaje'),
                    totalpresupuestado=Sum('total'),
                    proyeccion=Sum('proyeccion')
                ))
                total = total['totalpresupuestado']
                if total:
                    Presupuestocostos.objects.filter(
                        codcentrocostoxcuentacontable_new__codcuentacontable__cuentapadre=account, # NOQA
                        periodo=period
                    ).update(
                        porcentaje=F('total')/float(total)*100,
                        fechamodificacion=dt.datetime.today(),
                        usuariomodificacion=request.user
                    )

                messages.success(
                    request,
                    'Recalculo realizado con ??xito'
                )
            except Exception as e:
                messages.error(
                    request,
                    f'Exception no determinada: {e.__str__()}'
                )

        if request.POST.get('method') == 'apply-value':
            request.session['period'] = request.POST.get('period')
            request.session['account'] = request.POST.get('account')
            account = request.POST.get('account')
            period = request.POST.get('period')
            value = request.POST.get('value', '0').replace(',', '')
            result = try_convert_float(value)
            if type(result).__name__ == 'str':
                result = 0

            total = dict(Presupuestocostos.objects.filter(
                codcentrocostoxcuentacontable_new__codcuentacontable__cuentapadre=account,
                periodo=period
            ).aggregate(
                total_ejecutado_diciembre=Sum('ejecutadodiciembre'),
                porcentaje=Sum('porcentaje'),
                totalpresupuestado=Sum('total'),
                proyeccion=Sum('proyeccion')
            ))

            Presupuestocostos.objects.filter(
                codcentrocostoxcuentacontable_new__codcuentacontable__cuentapadre=account,
                periodo=period
            ).update(
                porcentaje=F('ejecutadodiciembre') / dc(
                    total['total_ejecutado_diciembre']
                )*100,
                fechamodificacion=dt.datetime.today(),
                usuariomodificacion=request.user
            )

            Presupuestocostos.objects.filter(
                codcentrocostoxcuentacontable_new__codcuentacontable__cuentapadre=account,
                periodo=period
            ).update(
                total=result * F('porcentaje') / 100
            )

            messages.success(
                request,
                'Aplicaci??n de valor realizado con ??xito'
            )

        if request.POST.get('method') == 'percentage':
            request.session['period'] = request.POST.get('period')
            request.session['account'] = request.POST.get('account')
            account = request.POST.get('account')
            period = request.POST.get('period')
            percentage = float(request.POST.get('percentage')) / 100
            if request.POST.get('btn-percentage') == 'Incrementar':
                Presupuestocostos.objects.filter(
                    codcentrocostoxcuentacontable_new__codcuentacontable__cuentapadre=account, # NOQA
                    periodo=period
                ).update(
                    total=(F('ejecutadodiciembre')+F('ejecutadodiciembre')*percentage),
                    porcentaje=0,
                    fechamodificacion=dt.datetime.today(),
                    usuariomodificacion=request.user
                )
                messages.success(
                    request,
                    'Incrementar procentaje realizado con ??xito'
                )
            elif request.POST.get('btn-percentage') == 'Decrementar':
                Presupuestocostos.objects.filter(
                    codcentrocostoxcuentacontable_new__codcuentacontable__cuentapadre=account, # NOQA
                    periodo=period
                ).update(
                    total=(F('ejecutadodiciembre')-F('ejecutadodiciembre')*percentage),
                    porcentaje=0,
                    fechamodificacion=dt.datetime.today(),
                    usuariomodificacion=request.user
                )
                messages.success(
                    request,
                    'Decrementar procentaje realizado con ??xito'
                )

    elif request.method == 'GET':
        if request.GET.get('period') and request.GET.get('account'):
            request.session['period'] = request.GET.get('period')
            request.session['account'] = request.GET.get('account')

    periods = Periodo.objects.filter(habilitado=True)
    query = (
        "SELECT distinct (cc.DescCuentaContable),cc.CodigoCuentaContable,c.Nivel, "
        "c.CuentaPadre from CuentasContables c INNER JOIN CuentasContables cc on "
        "cc.CodigoCuentaContable= c.CuentaPadre WHERE c.CodTipoCuenta= 7 and c.Nivel=7"
    )
    result = execute_sql_query(query)
    if result.get('status') == 'ok':
        accounts = result.get('data')
    else:
        accounts = []
        messages.warning(request, "No se pudo cargar cuentas padres")

    ctx = {
        'periods': periods,
        'accounts': accounts
    }

    if (
        request.session.get('period', None) and
        request.session.get('account', None)
    ):
        account = request.session.get('account')
        period = request.session.get('period')
        qs = Presupuestocostos.objects.filter(
            codcentrocostoxcuentacontable_new__codcuentacontable__cuentapadre=account,
            periodo=period
        ).order_by('-pk')
        total = Presupuestocostos.objects.filter(
            codcentrocostoxcuentacontable_new__codcuentacontable__cuentapadre=account,
            periodo=period
        ).aggregate(
            total_ejecutado_diciembre=Sum('ejecutadodiciembre'),
            porcentaje=Sum('porcentaje'),
            totalpresupuestado=Sum('total'),
            proyeccion=Sum('proyeccion')
        )

        if qs.first():
            month_projection = MONTH.get(int(qs.first().mesproyeccion))
        else:
            month_projection = ''
        ctx['qs'] = qs
        ctx['total'] = total
        ctx['month_projection'] = month_projection
    return render(request, 'cost_budget_register.html', ctx)


@login_required()
def cost_budget_generate_excel_file(request, period, account):
    qs = Presupuestocostos.objects.filter(
        codcentrocostoxcuentacontable_new__codcuentacontable__cuentapadre=account,
        periodo=period
    )
    return generate_excel_file_format(qs)
