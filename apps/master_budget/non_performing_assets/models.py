from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from apps.main.models import (
    Periodo, Detallexpresupuestoinversion, Cuentascontables
)
from apps.master_budget.models import (
    MasterParameters, AuditDataMixin, AmountMonthlyMixin, AmountIncreasesMonthlyMixin
)

from utils.constants import OTHERS_ASSETS_CRITERIA


class NonPerformingAssetsCategory(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    name = models.CharField(null=True, blank=True, max_length=50, db_column="Nombre")
    is_active = models.BooleanField(
        null=True, blank=True, default=True, db_column="Estado"
    )
    identifier = models.CharField(
        null=True, blank=True, max_length=150, db_column="Identificador"
    )
    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        null=True,
        blank=True,
        related_name="user_update_non_performing_assets_category",
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroActivosFijosCat"

    def __str__(self):
        return f"{self.name}"


class NonPerformingAssetsCategoryMapAccounts(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    category_id = models.ForeignKey(
        NonPerformingAssetsCategory,
        models.DO_NOTHING,
        db_column="CategoriaId",
        null=True,
        blank=True,
    )
    account_id = models.ForeignKey(
        Cuentascontables,
        models.DO_NOTHING,
        db_column="CuentaContableId",
        null=True,
        blank=True
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroActivosFijosCatXCuentasContables"


class NonPerformingAssetsScenario(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column='Id')
    period_id = models.ForeignKey(
        Periodo, models.DO_NOTHING, db_column="PeriodoId", null=True, blank=True
    )
    parameter_id = models.ForeignKey(
        MasterParameters, models.DO_NOTHING, db_column="ParametroId"
    )
    correlative = models.CharField(
        null=True, blank=True, max_length=50, db_column="Correlativo"
    )
    comment = models.CharField(
        null=True, blank=True, max_length=500, db_column="Comentario"
    )
    is_active = models.BooleanField(
        null=True, blank=True, default=True, db_column="Estado"
    )
    deleted = models.BooleanField(
        null=True, blank=True, default=False, db_column="Eliminado"
    )
    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        related_name="user_upd_non_performing_assets_scenario",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroActivosFijosEsc"


class BudgetedNonProductiveAssets(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column='Id')
    scenario_id = models.ForeignKey(
        NonPerformingAssetsScenario,
        models.DO_NOTHING,
        db_column="EscenarioId",
        null=True,
        blank=True
    )
    budgeted_asset_id = models.ForeignKey(
        Detallexpresupuestoinversion,
        models.DO_NOTHING,
        db_column="ActivoPresupuestadoId",
        null=True,
        blank=True
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroActivosFijosPresupuestados"


class NonPerformingAssetsXCategory(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column='Id')
    category_id = models.ForeignKey(
        NonPerformingAssetsCategory,
        models.DO_NOTHING,
        db_column="CategoriaId",
        null=True,
        blank=True
    )
    scenario_id = models.ForeignKey(
        NonPerformingAssetsScenario,
        models.DO_NOTHING,
        db_column="EscenarioId",
        null=True,
        blank=True
    )
    total_accumulated_balance = models.DecimalField(
        db_column="SaldoTotalAcumulado",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    accumulated_depreciation_balance = models.DecimalField(
        db_column="SaldoDepreciacionAcumulado",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    depreciation_balance = models.DecimalField(
        db_column="SaldoDepreciacion",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    total_net_balance = models.DecimalField(
        db_column="SaldoTotalNeto",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    comment_increases = models.CharField(
        db_column="ComentarioAumento",
        max_length=200,
        blank=True,
        null=True,
        default=""
    )
    comment_decreases = models.CharField(
        db_column="ComentarioDisminucion",
        max_length=200,
        blank=True,
        null=True,
        default=""
    )
    amount_increases = models.DecimalField(
        db_column="MontoAumento",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    amount_decreases = models.DecimalField(
        db_column="MontoDisminucion",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    month_decreases = models.IntegerField(
        db_column="MesesDisminucion", blank=True, null=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    month_increases = models.IntegerField(
        db_column="MesesAumento", blank=True, null=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    new_total_balance = models.DecimalField(
        db_column="NuevoSaldoTotal",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    new_depreciation_balance = models.DecimalField(
        db_column="NuevoSaldoDepreciacion",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroActivosFijosXCategoria"

    @property
    def depreciation_expense(self):
        return (
            self.accumulated_depreciation_balance +
            self.depreciation_balance +
            self.new_depreciation_balance
        )

    @property
    def total_net_balance_budgeted(self):
        total_subtract = (
            self.amount_decreases +
            self.depreciation_balance +
            self.new_depreciation_balance
        )
        total_add = self.total_net_balance + self.new_total_balance + self.amount_increases
        return total_add - total_subtract

    @property
    def sum_total_depreciation_expense(self):
        acumulated = 0
        for item in NonPerformingAssetsXCategory.objects.filter(
            scenario_id=self.scenario_id
        ):
            acumulated = acumulated + (
                item.accumulated_depreciation_balance +
                item.depreciation_balance +
                item.new_depreciation_balance
            )
        return acumulated

    @property
    def sum_total_net_balance_budgeted(self):
        acumulated = 0
        for item in NonPerformingAssetsXCategory.objects.filter(
            scenario_id=self.scenario_id
        ):
            total_subtract = (
                item.amount_decreases +
                item.depreciation_balance +
                item.new_depreciation_balance
            )
            total_add = (
                item.total_net_balance +
                item.new_total_balance +
                item.amount_increases
            )
            result = total_add - total_subtract
            acumulated = acumulated + result
        return acumulated


class OtherAssetsCategory(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    name = models.CharField(null=True, blank=True, max_length=50, db_column="Nombre")
    is_active = models.BooleanField(
        null=True, blank=True, default=True, db_column="Estado"
    )
    identifier = models.CharField(
        null=True, blank=True, max_length=150, db_column="Identificador"
    )
    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        null=True,
        blank=True,
        related_name="user_update_others_assets_category",
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroOtrosActivosCat"

    def __str__(self):
        return f"{self.name}"


class OtherAssetsScenario(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column='Id')
    period_id = models.ForeignKey(
        Periodo, models.DO_NOTHING, db_column="PeriodoId", null=True, blank=True
    )
    parameter_id = models.ForeignKey(
        MasterParameters, models.DO_NOTHING, db_column="ParametroId"
    )
    correlative = models.CharField(
        null=True, blank=True, max_length=50, db_column="Correlativo"
    )
    comment = models.CharField(
        null=True, blank=True, max_length=500, db_column="Comentario"
    )
    is_active = models.BooleanField(
        null=True, blank=True, default=True, db_column="Estado"
    )
    deleted = models.BooleanField(
        null=True, blank=True, default=False, db_column="Eliminado"
    )
    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        related_name="user_upd_others_assets_scenario",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroOtrosActivosEsc"


class OtherAssets(AuditDataMixin, AmountMonthlyMixin, AmountIncreasesMonthlyMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    scenario_id = models.ForeignKey(
        OtherAssetsScenario, models.DO_NOTHING, db_column="EscenarioId",
        null=True, blank=True,
    )
    category_id = models.ForeignKey(
        OtherAssetsCategory, models.DO_NOTHING, db_column="CategoriaId",
        blank=True, null=True
    )
    category = models.IntegerField(db_column="Categoria", null=True, blank=True)
    category_name = models.CharField(
        db_column="CategoriaNombre", max_length=150, null=True, blank=True
    )
    previous_balance = models.DecimalField(
        db_column="SaldoAnterior", decimal_places=2, max_digits=23,
        default=0, blank=True, null=True
    )
    criteria = models.IntegerField(
        db_column="Criterio", choices=OTHERS_ASSETS_CRITERIA,
        null=True, blank=True
    )
    comment = models.CharField(
        db_column="Comentario", max_length=200, default='',
        null=True, blank=True
    )
    percentage = models.FloatField(db_column="Procentaje", null=True, blank=True, default=0) # NOQA
    new_balance = models.DecimalField(
        db_column="NuevoSaldo", max_digits=23, decimal_places=2,
        default=0, blank=True, null=True
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroOtrosActivos"
