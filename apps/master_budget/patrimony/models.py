from django.db import models
from django.contrib.auth.models import User
from apps.main.models import Periodo

from apps.master_budget.models import (
    AuditDataMixin, AmountMonthlyMixin, AmountIncreasesMonthlyMixin,
    MasterParameters
)
from utils.constants import OTHERS_ASSETS_CRITERIA


def is_percentage(value):
    if value >= 0 and value <= 1:
        return True
    return False


class EquityCategory(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    name = models.CharField(null=True, blank=True, max_length=50, db_column="Nombre")
    is_active = models.BooleanField(null=True, blank=True, default=True, db_column="Estado")
    identifier = models.CharField(null=True, blank=True, max_length=150, db_column="Identificador")
    created_by = models.ForeignKey(User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True) # NOQA
    updated_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="ActualizadoPor", null=True, blank=True,
        related_name="user_update_equity_category"
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPatrimonioCat"

    def __str__(self):
        return f"{self.name}"


class EquityScenario(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column='Id')
    period_id = models.ForeignKey(Periodo, models.DO_NOTHING, db_column="PeriodoId", null=True, blank=True) # NOQA
    parameter_id = models.ForeignKey(MasterParameters, models.DO_NOTHING, db_column="ParametroId")
    correlative = models.CharField(null=True, blank=True, max_length=50, db_column="Correlativo")
    comment = models.CharField(null=True, blank=True, max_length=500, db_column="Comentario")
    is_active = models.BooleanField(null=True, blank=True, default=True, db_column="Estado")
    deleted = models.BooleanField(null=True, blank=True, default=False, db_column="Eliminado")
    created_by = models.ForeignKey(User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True) # NOQA
    updated_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="ActualizadoPor", null=True, blank=True,
        related_name="user_upd_equity_scenario"
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPatrimonioEsc"


class Equity(AuditDataMixin, AmountMonthlyMixin, AmountIncreasesMonthlyMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    scenario_id = models.ForeignKey(
        EquityScenario, models.DO_NOTHING, db_column="EscenarioId", null=True, blank=True
    )
    category_id = models.ForeignKey(
        EquityCategory, models.DO_NOTHING, db_column="CategoriaId", blank=True, null=True
    )
    category = models.IntegerField(db_column="Categoria", null=True, blank=True)
    category_name = models.CharField(db_column="CategoriaNombre", max_length=150, null=True, blank=True) # NOQA
    previous_balance = models.DecimalField(
        db_column="SaldoAnterior", decimal_places=2, max_digits=23, default=0, blank=True, null=True
    )
    criteria = models.IntegerField(db_column="Criterio", choices=OTHERS_ASSETS_CRITERIA, null=True, blank=True) # NOQA
    comment = models.CharField(db_column="Comentario", max_length=200, default='', null=True, blank=True) # NOQA
    percentage = models.FloatField(db_column="Procentaje", null=True, blank=True, default=0) # NOQA
    new_balance = models.DecimalField(
        db_column="NuevoSaldo", max_digits=23, decimal_places=2, default=0, blank=True, null=True
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPatrimonio"


class SurplusCategory(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column='Id')
    name = models.CharField(null=False, blank=False, max_length=100, db_column="Nombre")
    order = models.IntegerField(db_column="Orden", null=False, blank=False)
    action = models.CharField(null=False, blank=False, max_length=5, db_column="Accion")

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroCategoriaExcedentes"
        ordering = ('order',)

    def __str__(self):
        return self.name


class DistributionSurplusPeriod(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column='Id')
    period_id = models.ForeignKey(
        Periodo, models.DO_NOTHING, db_column="IdPeriodo", null=False, blank=False
    )
    surplus_amount = models.DecimalField(
        db_column="MontoExcedentes", decimal_places=2, max_digits=18, default=0, null=False,
        blank=False
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroDistribucionExcedentesPeriodo"


class DistributionSurplusCategory(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column='Id')
    id_surplus_category = models.ForeignKey(
        SurplusCategory, models.DO_NOTHING, db_column="IdCategoriaExcedentes", null=False,
        blank=False
    )
    id_dsp = models.ForeignKey(
        DistributionSurplusPeriod, models.DO_NOTHING, db_column="IdDEP", null=False, blank=False
    )
    title = models.CharField(db_column="Etiqueta", null=False, blank=False, max_length=100)
    percentage = models.FloatField(
       db_column="Porcentaje", null=False, blank=False, default=0,
       validators=[is_percentage]
    )
    amount = models.DecimalField(
        db_column="Monto", decimal_places=2, max_digits=18, default=0, blank=False, null=False
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroDistribucionExcedentesCategoria"
