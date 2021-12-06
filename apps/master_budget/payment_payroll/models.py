from django.db import models
from django.contrib.auth.models import User

from apps.main.models import (
    Periodo,
    Detallexpresupuestopersonal,
    Centroscosto
)
from apps.master_budget.models import (
    AuditDataMixin,
    PercentageIncreasesMonthlyMixin,
    AmountMonthlyMixin,
    AmountMonthlyMixinTemporal,
    MasterParameters
)


class PaymentPayrollScenario(
    AuditDataMixin,
    PercentageIncreasesMonthlyMixin
):
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
        related_name="user_upd_payment_payroll_scenario",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPagoPlanillaEsc"


class BudgetedPaymentPayroll(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column='Id')
    scenario_id = models.ForeignKey(
        PaymentPayrollScenario,
        models.DO_NOTHING,
        db_column="EscenarioId",
        null=True,
        blank=True
    )
    budgeted_id = models.ForeignKey(
        Detallexpresupuestopersonal,
        models.DO_NOTHING,
        db_column="PersonalPresupuestadoId",
        null=True,
        blank=True
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPersonalPresupuestados"


class PaymentPayroll(
    AmountMonthlyMixin,
    AmountMonthlyMixinTemporal,
    PercentageIncreasesMonthlyMixin
):
    id = models.AutoField(primary_key=True, db_column='Id')
    scenario_id = models.ForeignKey(
        PaymentPayrollScenario,
        models.DO_NOTHING,
        db_column="EscenarioId",
        null=True,
        blank=True
    )
    cost_center_id = models.ForeignKey(
        Centroscosto,
        models.DO_NOTHING,
        db_column="CentroCostoId",
        null=True,
        blank=True
    )
    permanent_amount_initial = models.DecimalField(
        db_column="MontoPermanenteInicial",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    adjusted_permanent_amount = models.DecimalField(
        db_column="MontoPermanenteAjustado",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    amount_initial_temp = models.DecimalField(
        db_column="MontoInicialTemporal",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )

    class Meta:
        default_permissions = []
        db_table = 'pptoMaestroPagoPlanilla'
