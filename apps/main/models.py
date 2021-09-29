from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from utils.constants import ZONES


class Administracionpresupuesto(models.Model):
    codadministracionpresupuesto = models.AutoField(
        db_column="CodAdministracionPresupuesto", primary_key=True
    )
    cerrarpresupuesto = models.BooleanField(
        db_column="CerrarPresupuesto"
    )

    class Meta:
        db_table = "AdministracionPresupuesto"


class Periodo(models.Model):
    codperiodo = models.AutoField(
        db_column="CodPeriodo", primary_key=True
    )
    descperiodo = models.CharField(
        db_column="DescPeriodo", max_length=100, blank=True, null=True
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True, auto_now=True
    )
    usuariocreacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioCreacion"
    )
    fechamodificacion = models.DateTimeField(
        db_column="FechaModificacion", blank=True, null=True
    )
    usuariomodificacion = models.IntegerField(
        db_column="UsuarioModificacion", blank=True, null=True
    )
    fechalimite = models.DateTimeField(
        db_column="FechaLimite", blank=True, null=True
    )
    habilitado = models.BooleanField(
        db_column="Habilitado"
    )
    cerrado = models.BooleanField(db_column="Cerrado")

    class Meta:
        db_table = "Periodo"
        ordering = ("-descperiodo", "-fechalimite",)

    def __str__(self):
        return "%s" % (self.descperiodo)


class Centrocostoxcuentacontable(models.Model):
    codcentrocostoxcuentacontable = models.AutoField(
        db_column="CodCentroCostoXCuentaContable", primary_key=True
    )
    codcentrocosto = models.ForeignKey(
        "Centroscosto",
        models.DO_NOTHING,
        db_column="CodCentroCosto",
        blank=True,
        null=True,
    )
    codcuentacontable = models.ForeignKey(
        "Cuentascontables",
        models.DO_NOTHING,
        db_column="CodCuentaContable",
        blank=True,
        null=True,
    )
    habilitado = models.BooleanField(
        db_column="Habilitado"
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True, auto_now=True
    )
    usuariocreacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioCreacion"
    )
    fechamodificacion = models.DateTimeField(
        db_column="FechaModificacion", blank=True, null=True
    )
    usuariomodificacion = models.IntegerField(
        db_column="UsuarioModificacion", blank=True, null=True
    )
    periodo = models.IntegerField(
        db_column="Periodo", blank=True, null=True
    )

    class Meta:
        db_table = "CentroCostoXCuentaContable"


class Centroscosto(models.Model):
    codcentrocosto = models.AutoField(
        db_column="CodCentroCosto", primary_key=True
    )
    codigocentrocosto = models.CharField(
        db_column="CodigoCentroCosto", max_length=50, blank=True, null=True
    )
    desccentrocosto = models.CharField(
        db_column="DescCentroCosto", max_length=150, blank=True, null=True
    )
    metropolitana = models.IntegerField(
        db_column="Metropolitana", blank=True, null=True
    )
    habilitado = models.BooleanField(
        db_column="Habilitado"
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True, auto_now=True
    )
    usuariocreacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioCreacion"
    )
    fechamodificacion = models.DateTimeField(
        db_column="FechaModificacion", blank=True, null=True
    )
    usuariomodificacion = models.IntegerField(
        db_column="UsuarioModificacion", blank=True, null=True
    )
    agencia = models.CharField(
        db_column="Agencia", max_length=5, blank=True, null=True
    )

    class Meta:
        db_table = "CentrosCosto"
        ordering = ("desccentrocosto",)

    def __unicode__(self):
        return "%s" % (self.desccentrocosto)

    def __str__(self):
        return "%s" % (self.desccentrocosto)


class Cuentascontables(models.Model):
    codcuentacontable = models.AutoField(
        db_column="CodCuentaContable", primary_key=True
    )
    codigocuentacontable = models.CharField(
        db_column="CodigoCuentaContable", max_length=50, blank=True, null=True
    )
    desccuentacontable = models.CharField(
        db_column="DescCuentaContable", max_length=150, blank=True, null=True
    )
    habilitado = models.BooleanField(
        db_column="Habilitado"
    )
    codtipocuenta = models.ForeignKey(
        "Tiposcuenta",
        models.DO_NOTHING,
        db_column="CodTipoCuenta",
        blank=True,
        null=True,
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True, auto_now=True
    )
    usuariocreacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioCreacion"
    )
    fechamodificacion = models.DateTimeField(
        db_column="FechaModificacion", blank=True, null=True
    )
    usuariomodificacion = models.IntegerField(
        db_column="UsuarioModificacion", blank=True, null=True
    )
    nivel = models.SmallIntegerField(db_column="Nivel", blank=True, null=True)
    cuentapadre = models.CharField(
        db_column="CuentaPadre", max_length=16, blank=True, null=True
    )

    class Meta:
        db_table = "CuentasContables"
        ordering = ("desccuentacontable",)

    def __unicode__(self):
        return "%s" % (self.desccuentacontable)

    def __str__(self):
        return "%s" % (self.desccuentacontable)


class Presupuestos(models.Model):
    codpresupuesto = models.AutoField(
        db_column="CodPresupuesto", primary_key=True
    )
    codperiodo = models.ForeignKey(
        "Periodo", models.DO_NOTHING, db_column="CodPeriodo", blank=True, null=True
    )
    enero = models.DecimalField(
        db_column="Enero", max_digits=17, decimal_places=2, blank=True, null=True
    )
    febrero = models.DecimalField(
        db_column="Febrero", max_digits=17, decimal_places=2, blank=True, null=True
    )
    marzo = models.DecimalField(
        db_column="Marzo", max_digits=17, decimal_places=2, blank=True, null=True
    )
    abril = models.DecimalField(
        db_column="Abril", max_digits=17, decimal_places=2, blank=True, null=True
    )
    mayo = models.DecimalField(
        db_column="Mayo", max_digits=17, decimal_places=2, blank=True, null=True
    )
    junio = models.DecimalField(
        db_column="Junio", max_digits=17, decimal_places=2, blank=True, null=True
    )
    julio = models.DecimalField(
        db_column="Julio", max_digits=17, decimal_places=2, blank=True, null=True
    )
    agosto = models.DecimalField(
        db_column="Agosto", max_digits=17, decimal_places=2, blank=True, null=True
    )
    septiembre = models.DecimalField(
        db_column="Septiembre", max_digits=17, decimal_places=2, blank=True, null=True
    )
    octubre = models.DecimalField(
        db_column="Octubre", max_digits=17, decimal_places=2, blank=True, null=True
    )
    noviembre = models.DecimalField(
        db_column="Noviembre", max_digits=17, decimal_places=2, blank=True, null=True
    )
    diciembre = models.DecimalField(
        db_column="Diciembre", max_digits=17, decimal_places=2, blank=True, null=True
    )
    montooriginal = models.DecimalField(
        db_column="MontoOriginal",
        max_digits=17,
        decimal_places=2,
        blank=True,
        null=True,
    )
    criterio = models.ForeignKey(
        "Criterios", models.DO_NOTHING, db_column="Criterio", blank=True, null=True
    )
    justificacion = models.TextField(
        db_column="Justificacion", blank=True, null=True
    )
    # totalpresupuestado = models.DecimalField(
    #     db_column='TotalPresupuestado',
    #     max_digits=28,
    #     decimal_places=2,
    #     blank=True,
    #     null=True
    # )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True, auto_now=True
    )
    usuariocreacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioCreacion"
    )
    fechamodificacion = models.DateTimeField(
        db_column="FechaModificacion", blank=True, null=True
    )
    usuariomodificacion = models.IntegerField(
        db_column="UsuarioModificacion", blank=True, null=True
    )
    codcentroscostoxcuentacontable = models.ForeignKey(
        Centrocostoxcuentacontable,
        models.DO_NOTHING,
        db_column="CodCentrosCostoXCuentaContable",
        blank=True,
        null=True,
    )
    estado = models.IntegerField(
        db_column="Estado", blank=True, null=True
    )
    codtipopresupuesto = models.ForeignKey(
        "Tipopresupuesto",
        models.DO_NOTHING,
        db_column="CodTipoPresupuesto",
        blank=True,
        null=True,
    )
    codproyecto = models.ForeignKey(
        "Proyectos", models.DO_NOTHING, db_column="CodProyecto", blank=True, null=True
    )
    saldonoviembre = models.DecimalField(
        db_column="SaldoNoviembre",
        max_digits=17,
        decimal_places=2,
        blank=True,
        null=True,
    )
    saldodiciembre = models.DecimalField(
        db_column="SaldoDiciembre",
        max_digits=17,
        decimal_places=2,
        blank=True,
        null=True,
    )

    etapasolicitado = models.DecimalField(
        db_column="EtapaSolicitado",
        max_digits=25,
        decimal_places=14,
        blank=True,
        null=True,
    )
    aprobadojuntadirectiva = models.DecimalField(
        db_column="AprobadoJuntaDirectiva",
        max_digits=25,
        decimal_places=14,
        blank=True,
        null=True,
    )
    aprobadogerencia = models.DecimalField(
        db_column="AprobadoGerencia",
        max_digits=25,
        decimal_places=14,
        blank=True,
        null=True,
    )
    aprobadoasamblea = models.DecimalField(
        db_column="AprobadoAsamblea",
        max_digits=25,
        decimal_places=14,
        blank=True,
        null=True,
    )
    mesproyeccion = models.CharField(
        db_column="MesProyeccion", max_length=100, blank=True, null=True
    )
    habilitado = models.BooleanField(
        db_column="Habilitado"
    )

    class Meta:
        managed = True
        db_table = "Presupuestos"


class Detallexpresupuestoinversion(models.Model):
    coddetallexpresupuesto = models.AutoField(
        db_column="CodDetalleXPresupuesto", primary_key=True
    )
    mes = models.CharField(
        db_column="Mes", max_length=100, blank=True, null=True
    )
    descproducto = models.CharField(
        db_column="DescProducto", max_length=25, blank=True, null=True
    )
    cantidad = models.IntegerField(
        db_column="Cantidad", blank=True, null=True
    )
    valor = models.DecimalField(
        db_column="Valor", max_digits=17, decimal_places=2, blank=True, null=True
    )
    presupuestado = models.DecimalField(
        db_column="Presupuestado",
        max_digits=23,
        decimal_places=5,
        blank=True,
        null=True,
    )
    codpresupuesto = models.ForeignKey(
        "Presupuestos",
        models.DO_NOTHING,
        db_column="CodPresupuesto",
        blank=True,
        null=True,
    )
    usuariocreacion = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="UsuarioCreacion",
        related_name="USUARIOCREACIONINVERSION",
    )
    usuariomodificacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioModificacion"
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True
    )
    fechamodificacion = models.DateTimeField(
        db_column="FechaModificacion", blank=True, null=True
    )
    estado = models.IntegerField(db_column="Estado", blank=True, null=True)
    # disponible = models.DecimalField(
    #     db_column='Disponible',
    #     max_digits=34,
    #     decimal_places=5,
    #     blank=True,
    #     null=True
    # )
    tipoaccion = models.ForeignKey(
        "Tipoaccionpresupuestoinversion",
        models.DO_NOTHING,
        db_column="TipoAccion",
        blank=True,
        null=True,
    )
    presupuestado = models.DecimalField(
        db_column="Presupuestado",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
    )
    aprobadojuntadirectiva = models.BooleanField(db_column="AprobadoJuntaDirectiva")
    aprobadojuntagerenciag = models.BooleanField(db_column="AprobadoJuntaGerenciaG")
    aprobadojuntaasamblea = models.BooleanField(db_column="AprobadoJuntaAsamblea")
    justificacion = models.TextField(
        db_column="Justificacion", blank=True, null=True
    )
    codcentrocostoxcuentacontable = models.ForeignKey(
        Centrocostoxcuentacontable,
        models.DO_NOTHING,
        db_column="CodCentroCostoXCuentaContable",
        blank=True,
        null=True,
    )
    periodo = models.ForeignKey(
        "Periodo", models.DO_NOTHING, db_column="Periodo", blank=True, null=True
    )
    habilitado = models.BooleanField(
        db_column="Habilitado"
    )
    reservado = models.DecimalField(
        db_column="Reservado", max_digits=23, decimal_places=5, blank=True, null=True
    )
    ejecutado = models.DecimalField(
        db_column="Ejecutado", max_digits=23, decimal_places=5, blank=True, null=True
    )
    presupuestadocontraslado = models.DecimalField(
        db_column="PresupuestadoConTraslado",
        max_digits=23,
        decimal_places=5,
        blank=True,
        null=True,
    )
    numerofusion = models.IntegerField(
        db_column="NumeroFusion", blank=True, null=True
    )
    valorfusion = models.DecimalField(
        db_column="ValorFusion", max_digits=23, decimal_places=5, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DetalleXPresupuestoInversion"

    def __unicode__(self):
        return "%s" % (self.descproducto)


class Detallexpresupuestopersonal(models.Model):
    coddetallexpresupuestopersonal = models.AutoField(
        db_column="CodDetalleXPresupuestoPersonal", primary_key=True
    )
    codpuesto = models.ForeignKey(
        "Puestos", models.DO_NOTHING, db_column="CodPuesto", blank=True, null=True
    )
    mes = models.CharField(
        db_column="Mes", max_length=150, blank=True, null=True
    )
    cantidad = models.IntegerField(
        db_column="Cantidad", blank=True, null=True
    )
    tipo = models.IntegerField(
        db_column="Tipo", blank=True, null=True
    )
    codcentrocosto = models.ForeignKey(
        Centroscosto,
        models.DO_NOTHING,
        db_column="CodCentroCosto",
        blank=True,
        null=True,
    )
    usuariocreacion = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="UsuarioCreacion",
        related_name="USUARIOCREACIONDETALLEXPERSONAL",
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True
    )
    usuariomodificacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioModificacion"
    )
    fechamodificacion = models.DateTimeField(
        db_column="FechaModificacion", blank=True, null=True
    )
    mesfin = models.CharField(db_column="MesFin", max_length=150, blank=True, null=True)
    sueldo = models.DecimalField(
        db_column="Sueldo", max_digits=23, decimal_places=5, blank=True, null=True
    )
    periodo = models.ForeignKey(
        "Periodo", models.DO_NOTHING, db_column="CodPeriodo", blank=True, null=True
    )
    justificacion = models.TextField(
        db_column="Justificacion", blank=True, null=True
    )
    tipoaccion = models.IntegerField(
        db_column="TipoAccion", blank=True, null=True
    )
    disponible = models.IntegerField(
        db_column="Disponible", blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "DetalleXPresupuestoPersonal"

    def get_tipo_name(self):
        return 'Temporal' if self.tipo == 1 else 'Permanente'


class Detallexpresupuestoviaticos(models.Model):
    coddetallexpresupuestoviaticos = models.AutoField(
        db_column="CodDetalleXPresupuestoViaticos", primary_key=True
    )
    codperiodo = models.ForeignKey(
        Periodo, models.DO_NOTHING, db_column="CodPeriodo", blank=True, null=True
    )
    filial = models.ForeignKey(
        "Filiales", models.DO_NOTHING, db_column="Filial", blank=True, null=True
    )
    categoria = models.CharField(
        db_column="Categoria", max_length=1, blank=True, null=True
    )
    cantidaddias = models.DecimalField(
        db_column="CantidadDias", max_digits=12, decimal_places=5, blank=True, null=True
    )
    tipoviatico = models.IntegerField(
        db_column="TipoViatico", blank=True, null=True
    )
    cantidadviajes = models.IntegerField(
        db_column="CantidadViajes", blank=True, null=True
    )
    codcentrocosto = models.ForeignKey(
        Centroscosto,
        models.DO_NOTHING,
        db_column="CodCentroCosto",
        blank=True,
        null=True,
    )
    usuariocreacion = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="UsuarioCreacion",
        related_name="USUARIOCREACIONDETALLEXPRESUPUESTOVIATICOS",
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True
    )
    usuariomodificacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioModificacion"
    )
    fechamodificacion = models.DateTimeField(
        db_column="FechaModificacion", blank=True, null=True
    )
    zona = models.CharField(db_column="Zona", max_length=1, blank=True, null=True)
    valor = models.DecimalField(
        db_column="Valor", max_digits=25, decimal_places=14, blank=True, null=True
    )
    presupuestado = models.DecimalField(
        db_column="Presupuestado",
        max_digits=25,
        decimal_places=14,
        blank=True,
        null=True,
    )
    tipoaccion = models.IntegerField(
        db_column="TipoAccion", blank=True, null=True
    )
    comentario = models.CharField(
        db_column="Comentario", max_length=100, blank=True, null=True
    )
    disponible = models.DecimalField(
        db_column="Disponible", max_digits=34, decimal_places=5, blank=True, null=True
    )
    justificacion = models.TextField(
        db_column="Justificacion", blank=True, null=True
    )

    habilitado = models.BooleanField(
        db_column="Habilitado"
    )

    class Meta:
        managed = True
        db_table = "DetalleXPresupuestoViaticos"

    @property
    def zona_desc(self):
        return ZONES.get(self.zona)


class Presupuestoindirecto(models.Model):
    codpresupuestoindirecto = models.AutoField(
        db_column="CodPresupuestoIndirecto", primary_key=True
    )
    codcentrocostoxcuentacontable = models.IntegerField(
        db_column="CodCentroCostoXCuentaContable", blank=True, null=True
    )
    valor = models.DecimalField(
        db_column="Valor", max_digits=17, decimal_places=2, blank=True, null=True
    )
    total = models.DecimalField(
        db_column="Total", max_digits=17, decimal_places=2, blank=True, null=True
    )
    habilitado = models.BooleanField(
        db_column="Habilitado"
    )
    periodo = models.ForeignKey(
        Periodo, models.DO_NOTHING, db_column="Periodo", blank=True, null=True
    )
    usuariocreacion = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="UsuarioCreacion",
        related_name="USUARIOCREACIONPRESUPUESTOINDIRECTO",
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True
    )
    usuariomodificacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioModificacion"
    )
    fechamodificacion = models.DateTimeField(
        db_column="FechaModificacion", blank=True, null=True
    )
    estado = models.IntegerField(
        db_column="Estado", blank=True, null=True
    )
    # aprobadojuntadirectiva = models.BooleanField(db_column='AprobadoJuntaDirectiva')
    # aprobadojuntagerenciag = models.BooleanField(db_column='AprobadoJuntaGerenciaG')
    # aprobadojuntaasamblea = models.BooleanField(db_column='AprobadoJuntaAsamblea')
    porcentaje = models.DecimalField(
        db_column="Porcentaje", max_digits=17, decimal_places=10, blank=True, null=True
    )
    ejecutadodiciembre = models.DecimalField(
        db_column="EjecutadoDiciembre",
        max_digits=25,
        decimal_places=14,
        blank=True,
        null=True,
    )
    codcentrocostoxcuentacontable_new = models.ForeignKey(
        Centrocostoxcuentacontable,
        models.DO_NOTHING,
        db_column="CodCentroCostoXCuentaContable_new",
        blank=True,
        null=True,
    )
    mesproyeccion = models.IntegerField(
        db_column="MesProyeccion", blank=True, null=True
    )
    proyeccion = models.DecimalField(
        db_column="Proyeccion", max_digits=17, decimal_places=2, blank=True, null=True
    )

    class Meta:
        db_table = "PresupuestoIndirecto"


class Presupuestoingresos(models.Model):
    codpresupuestoingresos = models.AutoField(
        db_column="CodPresupuestoIngresos", primary_key=True
    )
    codcentrocostoxcuentacontable = models.ForeignKey(
        Centrocostoxcuentacontable,
        models.DO_NOTHING,
        db_column="CodCentroCostoXCuentaContable",
        blank=True,
        null=True,
    )
    valor = models.DecimalField(
        db_column="Valor", max_digits=17, decimal_places=2, blank=True, null=True
    )
    total = models.DecimalField(
        db_column="Total", max_digits=17, decimal_places=2, blank=True, null=True
    )
    habilitado = models.BooleanField(
        db_column="Habilitado"
    )
    periodo = models.ForeignKey(
        Periodo, models.DO_NOTHING, db_column="Periodo", blank=True, null=True
    )
    usuariocreacion = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="UsuarioCreacion",
        related_name="USUARIOCREACIONPRESUPUESTOINGRESOS",
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True
    )
    usuariomodificacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioModificacion"
    )
    fechamodificacion = models.DateTimeField(
        db_column="FechaModificacion", blank=True, null=True
    )
    estado = models.IntegerField(
        db_column="Estado", blank=True, null=True
    )
    porcentaje = models.DecimalField(
        db_column="Porcentaje", max_digits=17, decimal_places=10, blank=True, null=True
    )
    ejecutadodiciembre = models.DecimalField(
        db_column="EjecutadoDiciembre",
        max_digits=25,
        decimal_places=14,
        blank=True,
        null=True,
    )
    codcentrocostoxcuentacontable_new = models.ForeignKey(
        Centrocostoxcuentacontable,
        models.DO_NOTHING,
        db_column="CodCentroCostoXCuentaContable_new",
        blank=True,
        null=True,
        related_name="NuevoIngreso",
    )
    mesproyeccion = models.IntegerField(
        db_column="MesProyeccion", blank=True, null=True
    )
    proyeccion = models.DecimalField(
        db_column="Proyeccion", max_digits=17, decimal_places=2, blank=True, null=True
    )

    class Meta:
        db_table = "PresupuestoIngresos"


class Presupuestocostos(models.Model):
    codpresupuestocostos = models.AutoField(
        db_column="CodPresupuestoCostos", primary_key=True
    )
    codcentrocostoxcuentacontable = models.ForeignKey(
        Centrocostoxcuentacontable,
        models.DO_NOTHING,
        db_column="CodCentroCostoXCuentaContable",
        blank=True,
        null=True,
    )
    valor = models.DecimalField(
        db_column="Valor", max_digits=17, decimal_places=2, blank=True, null=True
    )
    total = models.DecimalField(
        db_column="Total", max_digits=17, decimal_places=2, blank=True, null=True
    )
    habilitado = models.BooleanField(
        db_column="Habilitado"
    )
    periodo = models.ForeignKey(
        Periodo, models.DO_NOTHING, db_column="Periodo", blank=True, null=True
    )
    usuariocreacion = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="UsuarioCreacion",
        related_name="USUARIOCREACIONPRESUPUESTOCOSTOS",
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True
    )
    usuariomodificacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioModificacion"
    )
    fechamodificacion = models.DateTimeField(
        db_column="FechaModificacion", blank=True, null=True
    )
    estado = models.IntegerField(
        db_column="Estado", blank=True, null=True
    )
    aprobadojuntadirectiva = models.BooleanField(
        db_column="AprobadoJuntaDirectiva"
    )
    aprobadojuntagerenciag = models.BooleanField(
        db_column="AprobadoJuntaGerenciaG"
    )
    aprobadojuntaasamblea = models.BooleanField(
        db_column="AprobadoJuntaAsamblea"
    )
    porcentaje = models.DecimalField(
        db_column="Porcentaje", max_digits=17, decimal_places=10, blank=True, null=True
    )
    ejecutadodiciembre = models.DecimalField(
        db_column="EjecutadoDiciembre",
        max_digits=25,
        decimal_places=14,
        blank=True,
        null=True,
    )
    codcentrocostoxcuentacontable_new = models.ForeignKey(
        Centrocostoxcuentacontable,
        models.DO_NOTHING,
        db_column="CodCentroCostoXCuentaContable_new",
        blank=True,
        null=True,
        related_name="codcentrocostoxcuenta_nuevo_costos",
    )
    mesproyeccion = models.IntegerField(
        db_column="MesProyeccion", blank=True, null=True
    )
    proyeccion = models.DecimalField(
        db_column="Proyeccion", max_digits=17, decimal_places=2, blank=True, null=True
    )

    class Meta:
        db_table = "PresupuestoCostos"


class Proyectos(models.Model):
    codproyecto = models.AutoField(
        db_column="CodProyecto", primary_key=True
    )
    descproyecto = models.CharField(
        db_column="DescProyecto", max_length=100, blank=True, null=True
    )
    fechainicio = models.DateTimeField(
        db_column="FechaInicio", blank=True, null=True
    )
    fechafinal = models.DateTimeField(
        db_column="FechaFinal", blank=True, null=True
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True, auto_now=True
    )
    usuariocreacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioCreacion"
    )
    fechamodificacion = models.DateTimeField(
        db_column="FechaModificacion", blank=True, null=True
    )
    usuariomodificacion = models.IntegerField(
        db_column="UsuarioModificacion", blank=True, null=True
    )
    codcentrocosto = models.ForeignKey(
        Centroscosto,
        models.DO_NOTHING,
        db_column="CodCentroCosto",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "Proyectos"
        ordering = ("-fechainicio", "descproyecto", 'codcentrocosto',)

    def __str__(self):
        return "%s" % (self.descproyecto)


class Tipopresupuesto(models.Model):
    codtipopresupuesto = models.AutoField(
        db_column="CodTipoPresupuesto", primary_key=True
    )
    desctipopresupuesto = models.CharField(
        db_column="DescTipoPresupuesto", max_length=25, blank=True, null=True
    )

    class Meta:
        db_table = "TipoPresupuesto"

    def __unicode__(self):
        return "%s" % (self.desctipopresupuesto)


class Tiposcuenta(models.Model):
    codtipocuenta = models.AutoField(
        db_column="CodTipoCuenta", primary_key=True
    )
    desctipocuenta = models.CharField(
        db_column="DescTipoCuenta", max_length=100, blank=True, null=True
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True, auto_now=True
    )
    usuariocreacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioCreacion"
    )
    fechamodificacion = models.DateTimeField(
        db_column="FechaModificacion", blank=True, null=True
    )
    usuariomodificacion = models.IntegerField(
        db_column="UsuarioModificacion", blank=True, null=True
    )

    class Meta:
        db_table = "TiposCuenta"

    def __unicode__(self):
        return "%s" % (self.desctipocuenta)


class Puestos(models.Model):
    codpuesto = models.AutoField(
        db_column="CodPuesto", primary_key=True
    )
    descpuesto = models.CharField(
        db_column="DescPuesto", max_length=100, blank=True, null=True
    )
    sueldopermanente = models.DecimalField(
        db_column="SueldoPermanente",
        max_digits=25,
        decimal_places=2,
        blank=True,
        null=True,
    )
    sueldotemporal = models.DecimalField(
        db_column="SueldoTemporal",
        max_digits=25,
        decimal_places=2,
        blank=True,
        null=True,
    )
    puestoestado = models.BooleanField(db_column="puestoEstado")

    class Meta:
        db_table = "Puestos"

    def __unicode__(self):
        return "%s" % (self.descpuesto)

    def __str__(self):
        return "%s" % (self.descpuesto)


class Filiales(models.Model):
    codfilial = models.IntegerField(
        db_column="CodFilial", primary_key=True
    )
    nombrefilial = models.CharField(
        db_column="NombreFilial", max_length=100, blank=True, null=True
    )
    metropolitana = models.IntegerField(
        db_column="Metropolitana", blank=True, null=True
    )

    class Meta:
        db_table = "Filiales"

    def __unicode__(self):
        return "%s" % (self.nombrefilial)

    def __str__(self):
        return "%s" % (self.nombrefilial)


class ResponsablesPorCentrosCostos(models.Model):
    CodResponsable = models.AutoField(
        db_column="CodResponsable", primary_key=True
    )
    CodCentroCosto = models.ForeignKey(
        "CentrosCosto",
        models.DO_NOTHING,
        db_column="CodCentroCosto",
        blank=True,
        null=True,
    )
    CodUser = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="CodUser",
        blank=True,
        null=True,
    )
    Estado = models.BooleanField(db_column="Estado")

    class Meta:
        db_table = "ResponsablesPorCentrosCostos"
        ordering = ("CodCentroCosto", "CodUser", "Estado")
        unique_together = ('CodCentroCosto', 'CodUser',)


class Inversiones(models.Model):
    codinversion = models.AutoField(
        db_column="CodInversion", primary_key=True
    )
    descinversion = models.CharField(
        db_column="DescInversion", max_length=200, blank=True, null=True
    )
    codcuentacontable = models.ForeignKey(
        Cuentascontables,
        models.DO_NOTHING,
        db_column="CodCuentaContable",
        blank=True,
        null=True,
    )
    meses_depreciacion = models.IntegerField(
        db_column="MesesDepreciacion", blank=True, null=True
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True
    )
    usuariocreacion = models.IntegerField(
        db_column="UsuarioCreacion", blank=True, null=True
    )
    fechamodificacion = models.DateTimeField(
        db_column="FechaModificacion", blank=True, null=True
    )
    usuariomodificacion = models.IntegerField(
        db_column="UsuarioModificacion", blank=True, null=True
    )
    Habilitado = models.BooleanField(db_column="Habilitado")

    class Meta:
        db_table = "Inversiones"
        ordering = ("descinversion",)

    def __str__(self):
        return f'{self.descinversion}'


class Manejodeviaticos(models.Model):
    codmanejoviaticos = models.AutoField(
        db_column="CodManejoViaticos", primary_key=True
    )
    codcentrocosto = models.ForeignKey(
        Centroscosto,
        models.DO_NOTHING,
        db_column="CodCentroCosto",
        blank=True,
        null=True,
    )
    centropresupuestado = models.ForeignKey(
        Centroscosto,
        models.DO_NOTHING,
        db_column="CentroPresupuestado",
        blank=True,
        null=True,
        related_name="CENTORMANEJO",
    )
    presupuestado = models.DecimalField(
        db_column="Presupuestado",
        max_digits=23,
        decimal_places=5,
        blank=True,
        null=True,
    )
    presupuestadocontraslado = models.DecimalField(
        db_column="PresupuestadoConTraslado",
        max_digits=23,
        decimal_places=5,
        blank=True,
        null=True,
    )
    comentario = models.CharField(
        db_column="Comentario", max_length=200, blank=True, null=True
    )
    tipoaccion = models.IntegerField(
        db_column="TipoAccion", blank=True, null=True
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True
    )
    usuariocreacion = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="UsuarioCreacion",
        blank=True,
        null=True,
        related_name="ManejoViaticosUsuarioCreacion",
    )
    periodo = models.ForeignKey(
        "Periodo", models.DO_NOTHING, db_column="Periodo", blank=True, null=True
    )
    reservado = models.DecimalField(
        db_column="Reservado", max_digits=23, decimal_places=5, blank=True, null=True
    )
    ejecutado = models.DecimalField(
        db_column="Ejecutado", max_digits=23, decimal_places=5, blank=True, null=True
    )
    # disponible = models.DecimalField(
    #     db_column='Disponible',
    #     max_digits=25,
    #     decimal_places=5,
    #     blank=True,
    #     null=True
    # )

    class Meta:
        db_table = "ManejoDeViaticos"


class Historicotrasladosviaticos(models.Model):
    codhistoricotrasladosviaticos = models.AutoField(
        db_column="CodHistoricoTrasladosViaticos", primary_key=True
    )
    codorigen = models.ForeignKey(
        Detallexpresupuestoviaticos,
        models.DO_NOTHING,
        db_column="CodOrigen",
        blank=True,
        null=True,
        related_name="ORIGEN",
    )
    montoorigen = models.DecimalField(
        db_column="MontoOrigen", max_digits=23, decimal_places=5, blank=True, null=True
    )
    coddestino = models.ForeignKey(
        Detallexpresupuestoviaticos,
        models.DO_NOTHING,
        db_column="CodDestino",
        blank=True,
        null=True,
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True
    )
    comentario = models.CharField(
        db_column="Comentario", max_length=200, blank=True, null=True
    )

    class Meta:
        db_table = "HistoricoTrasladosViaticos"


class Manejopersonal(models.Model):
    codmanejopersonal = models.AutoField(
        db_column="CodManejoPersonal", primary_key=True
    )
    codpuesto = models.ForeignKey(
        "Puestos", models.DO_NOTHING, db_column="CodPuesto", blank=True, null=True
    )
    mesinicio = models.CharField(
        db_column="MesInicio", max_length=150, blank=True, null=True
    )
    mesfin = models.CharField(
        db_column="MesFin", max_length=150, blank=True, null=True
    )
    cantidad = models.IntegerField(
        db_column="Cantidad", blank=True, null=True
    )
    codcentrocosto = models.ForeignKey(
        Centroscosto,
        models.DO_NOTHING,
        db_column="CodCentroCosto",
        blank=True,
        null=True,
    )
    usuariocreacion = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="UsuarioCreacion",
        related_name="USUARIOCREACIONMANEJOPERSONAL",
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True
    )
    usuariomodificacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioModificacion"
    )
    codperiodo = models.ForeignKey(
        "Periodo", models.DO_NOTHING, db_column="CodPeriodo", blank=True, null=True
    )
    sueldo = models.DecimalField(
        db_column="Sueldo", max_digits=23, decimal_places=5, blank=True, null=True
    )
    comentario = models.CharField(
        db_column="Comentario", max_length=200, blank=True, null=True
    )

    class Meta:
        db_table = "ManejoPersonal"


class Historicotrasladosinversiones(models.Model):
    codhistoricotrasladosinversiones = models.AutoField(
        db_column="CodHistoricoTrasladosInversiones", primary_key=True
    )
    codorigen = models.ForeignKey(
        Detallexpresupuestoinversion,
        models.DO_NOTHING,
        db_column="CodOrigen",
        blank=True,
        null=True,
        related_name="ORIGEN",
    )
    montoorigen = models.DecimalField(
        db_column="MontoOrigen", max_digits=23, decimal_places=5, blank=True, null=True
    )
    coddestino = models.ForeignKey(
        Detallexpresupuestoinversion,
        models.DO_NOTHING,
        db_column="CodDestino",
        blank=True,
        null=True,
    )
    comentario = models.CharField(
        db_column="Comentario", max_length=200, blank=True, null=True
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True
    )
    fecha = models.DateTimeField(
        db_column="FechaAplicacion", blank=True, null=True
    )
    montotraslado = models.DecimalField(
        db_column="MontoTraslado",
        max_digits=23,
        decimal_places=5,
        blank=True,
        null=True,
    )
    montodestino = models.DecimalField(
        db_column="MontoDestino", max_digits=23, decimal_places=5, blank=True, null=True
    )
    montoorigendespues = models.DecimalField(
        db_column="MontoOrigenDespues",
        max_digits=23,
        decimal_places=5,
        blank=True,
        null=True,
    )
    montodestinodespues = models.DecimalField(
        db_column="MontoDestinoDespues",
        max_digits=23,
        decimal_places=5,
        blank=True,
        null=True,
    )
    periodo = models.IntegerField(
        db_column="Periodo", blank=True, null=True
    )

    class Meta:
        db_table = "HistoricoTrasladosInversiones"


class Transaccionesviaticos(models.Model):
    codtransaccionviatico = models.AutoField(
        db_column="CodTransaccionViatico", primary_key=True
    )
    codmanejoviatico = models.ForeignKey(
        Manejodeviaticos,
        models.DO_NOTHING,
        db_column="CodManejoViatico",
        blank=True,
        null=True,
    )
    requerido = models.DecimalField(
        db_column="Requerido", max_digits=23, decimal_places=5, blank=True, null=True
    )
    comprometido = models.DecimalField(
        db_column="Comprometido", max_digits=23, decimal_places=5, blank=True, null=True
    )
    numerosolicitud = models.CharField(
        db_column="NumeroSolicitud", max_length=100, blank=True, null=True
    )
    numeroliquidacion = models.CharField(
        db_column="NumeroLiquidacion", max_length=100, blank=True, null=True
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True
    )
    usuariocreacion = models.ForeignKey(
        User, models.DO_NOTHING, db_column="UsuarioCreacion"
    )
    comentario = models.TextField(
        db_column="Comentario", blank=True, null=True
    )

    class Meta:
        db_table = "TransaccionesViaticos"


class Transaccionesinversiones(models.Model):
    codtransaccioninversion = models.AutoField(
        db_column="CodTransaccionInversion", primary_key=True
    )
    coddetallexpresupuestoinversion = models.ForeignKey(
        Detallexpresupuestoinversion,
        models.DO_NOTHING,
        db_column="CodDetalleXPresupuestoInversion",
        blank=True,
        null=True,
    )
    requerido = models.DecimalField(
        db_column="Requerido", max_digits=23, decimal_places=5, blank=True, null=True
    )
    comprometido = models.DecimalField(
        db_column="Comprometido", max_digits=23, decimal_places=5, blank=True, null=True
    )
    numerosolicitud = models.IntegerField(
        db_column="NumeroSolicitud", blank=True, null=True
    )
    numeroliquidacion = models.IntegerField(
        db_column="NumeroLiquidacion", blank=True, null=True
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True
    )
    usuariocreacion = models.IntegerField(
        db_column="UsuarioCreacion", blank=True, null=True
    )
    comentario = models.TextField(
        db_column="Comentario", blank=True, null=True
    )

    class Meta:
        db_table = "TransaccionesInversiones"


class Valoresviativos(models.Model):
    categoria = models.CharField(
        db_column="Categoria", max_length=1
    )
    clasepersonal = models.CharField(
        db_column="ClasePersonal", max_length=50, blank=True, null=True
    )
    tipoviatico = models.SmallIntegerField(
        db_column="TipoViatico"
    )
    zona = models.CharField(
        db_column="Zona", max_length=1
    )
    valor = models.DecimalField(max_digits=17, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = "ValoresViativos"
        # unique_together = (('zona', 'tipoviatico', 'categoria'),)


class Criterios(models.Model):
    codcriterio = models.AutoField(
        db_column="CodCriterio", primary_key=True
    )
    descripcioncriterio = models.CharField(
        db_column="DescripcionCriterio", max_length=10, blank=True, null=True
    )
    valor = models.DecimalField(
        db_column="Valor", max_digits=23, decimal_places=5, blank=True, null=True
    )

    class Meta:
        db_table = "Criterios"

    def __unicode__(self):
        return "%s" % (self.descripcioncriterio)


class Tipoaccionpresupuestoinversion(models.Model):
    codtipoaccionpresupuestoinversion = models.AutoField(
        db_column="CodTipoAccionPresupuestoInversion", primary_key=True
    )
    descripciontipoaccion = models.CharField(
        db_column="DescripcionTipoAccion", max_length=100, blank=True, null=True
    )

    class Meta:
        db_table = "TipoAccionPresupuestoInversion"

    def __unicode__(self):
        return "%s" % (self.descripciontipoaccion)


class Historicotraslados(models.Model):
    codhistoricotraslado = models.AutoField(
        db_column="CodHistoricoTraslado", primary_key=True
    )
    montoorigengastos = models.DecimalField(
        db_column="MontoOrigenGastos",
        max_digits=25,
        decimal_places=5,
        blank=True,
        null=True,
    )
    codorigengastos = models.ForeignKey(
        "Presupuestos",
        models.DO_NOTHING,
        db_column="CodOrigenGastos",
        blank=True,
        null=True,
    )
    montoorigenindirecto = models.DecimalField(
        db_column="MontoOrigenIndirecto",
        max_digits=25,
        decimal_places=5,
        blank=True,
        null=True,
    )
    codorigenindirecto = models.ForeignKey(
        "Presupuestoindirecto",
        models.DO_NOTHING,
        db_column="CodOrigenIndirecto",
        blank=True,
        null=True,
    )
    montoorigencostos = models.DecimalField(
        db_column="MontoOrigenCostos",
        max_digits=25,
        decimal_places=5,
        blank=True,
        null=True,
    )
    codorigencostos = models.ForeignKey(
        "Presupuestocostos",
        models.DO_NOTHING,
        db_column="CodOrigenCostos",
        blank=True,
        null=True,
    )
    montodestino = models.DecimalField(
        db_column="MontoDestino", max_digits=25, decimal_places=5, blank=True, null=True
    )
    coddestinogastos = models.ForeignKey(
        "Presupuestos",
        models.DO_NOTHING,
        db_column="CodDestinoGastos",
        blank=True,
        null=True,
        related_name="CodigoDestinoGastos",
    )
    coddestinoindirecto = models.ForeignKey(
        "Presupuestoindirecto",
        models.DO_NOTHING,
        db_column="CodDestinoIndirecto",
        blank=True,
        null=True,
        related_name="CodigoDestinoIndirecto",
    )
    coddestinocostos = models.ForeignKey(
        "Presupuestocostos",
        models.DO_NOTHING,
        db_column="CodDestinoCostos",
        blank=True,
        null=True,
        related_name="CodigoDestinoCostos",
    )
    codusuario = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CodUsuario", blank=True, null=True
    )
    fechacreacion = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True
    )
    fechaaplicacion = models.DateTimeField(
        db_column="FechaAplicacion", blank=True, null=True
    )

    class Meta:
        db_table = "HistoricoTraslados"
