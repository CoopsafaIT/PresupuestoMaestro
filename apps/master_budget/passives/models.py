from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.main.models import Periodo
from apps.master_budget.models import (
    AuditDataMixin,
    CommentMixin,
    GrowthPercentageMonthlyMixin,
    RateMonthlyMixin,
    TermMonthlyMixin,
    MasterParameters
)
from utils.constants import MONTH_CHOICES


class SavingsLiabilitiesCategory(AuditDataMixin):
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
        related_name="user_update_savings_liabilities_category",
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPasivoAhorroCat"

    def __str__(self):
        return f"{self.name}"


class SavingsLiabilitiesScenario(
    AuditDataMixin,
    GrowthPercentageMonthlyMixin,
    RateMonthlyMixin,
):
    id = models.AutoField(primary_key=True, db_column="Id")
    period_id = models.ForeignKey(
        Periodo, models.DO_NOTHING, db_column="PeriodoId", null=True, blank=True
    )
    parameter_id = models.ForeignKey(
        MasterParameters, models.DO_NOTHING, db_column="ParametroId"
    )
    category_id = models.ForeignKey(
        SavingsLiabilitiesCategory, models.DO_NOTHING, db_column="CategoriaId"
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
    base_amount = models.DecimalField(
        db_column="MontoBase", max_digits=23, decimal_places=2, null=True, blank=True
    )
    annual_growth_amount = models.DecimalField(
        db_column="MontoCrecimientoAnual",
        max_digits=23,
        decimal_places=2,
        null=True,
        blank=True,
    )

    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        related_name="user_upd_savings_liabilities_scenario",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPasivoAhorroEsc"


@receiver(post_save, sender=SavingsLiabilitiesScenario)
def post_save_savings_liabilities(sender, instance, created, **kwargs):
    if created:
        qs = SavingsLiabilitiesScenario.objects.get(pk=instance.pk)
        for item in range(1, 13):
            SavingsLiabilities.objects.create(scenario_id=qs, month=item)


class SavingsLiabilitiesComment(CommentMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    scenario_id = models.ForeignKey(
        SavingsLiabilitiesScenario,
        models.DO_NOTHING,
        db_column="EscenarioId",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPasivoAhorroMsj"


class SavingsLiabilities(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")

    scenario_id = models.ForeignKey(
        SavingsLiabilitiesScenario,
        models.DO_NOTHING,
        db_column="EscenarioId",
        null=True,
        blank=True,
    )
    month = models.IntegerField(
        db_column="Mes", null=True, blank=True, choices=MONTH_CHOICES
    )
    amount_initial = models.DecimalField(
        db_column="MontoInicial",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    percent_growth = models.FloatField(
        db_column="PorcentajeCrecimiento", blank=True, null=True, default=0
    )
    amount_growth = models.DecimalField(
        db_column="MontoCrecimiento",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    new_amount = models.DecimalField(
        db_column="MontoTotalCrecimiento",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    rate = models.FloatField(db_column="Tasa", blank=True, null=True, default=0)
    total_interest = models.DecimalField(
        db_column="InteresesGenerado",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    comment = models.CharField(
        null=True, blank=True, max_length=500, db_column="Comentario"
    )
    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        related_name="user_upd_savings_liabilities",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPasivoAhorro"

    def __str__(self):
        return f"{self.month}"


class LiabilitiesLoansCategory(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    name = models.CharField(null=True, blank=True, max_length=50, db_column="Nombre")
    is_active = models.BooleanField(
        null=True, blank=True, default=True, db_column="Estado"
    )
    identifier = models.CharField(
        null=True, blank=True, max_length=50, db_column="Identificador"
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
        related_name="user_update_liabilities_loans_category",
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPasivoPrestamosCat"

    def __str__(self):
        return f"{self.name}"


class LiabilitiesLoansScenario(
    AuditDataMixin,
    GrowthPercentageMonthlyMixin,
    TermMonthlyMixin,
    RateMonthlyMixin,
):
    id = models.AutoField(primary_key=True, db_column="Id")
    period_id = models.ForeignKey(
        Periodo, models.DO_NOTHING, db_column="PeriodoId", null=True, blank=True
    )
    parameter_id = models.ForeignKey(
        MasterParameters, models.DO_NOTHING, db_column="ParametroId"
    )
    category_id = models.ForeignKey(
        LiabilitiesLoansCategory, models.DO_NOTHING, db_column="CategoriaId"
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
    base_amount = models.DecimalField(
        db_column="MontoBase", max_digits=23, decimal_places=2, null=True, blank=True
    )
    annual_growth_amount = models.DecimalField(
        db_column="MontoCrecimientoAnual",
        max_digits=23,
        decimal_places=2,
        null=True,
        blank=True,
    )

    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        related_name="user_upd_liabilities_loans_scenario",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPasivoPrestamosEsc"


@receiver(post_save, sender=LiabilitiesLoansScenario)
def post_save_liabilities_loans(sender, instance, created, **kwargs):
    if created:
        qs = LiabilitiesLoansScenario.objects.get(pk=instance.pk)
        for item in range(1, 13):
            LiabilitiesLoans.objects.create(scenario_id=qs, month=item)


class LiabilitiesLoansComment(CommentMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    scenario_id = models.ForeignKey(
        LiabilitiesLoansScenario,
        models.DO_NOTHING,
        db_column="EscenarioId",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPasivoPrestamosMsj"


class LiabilitiesLoans(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    scenario_id = models.ForeignKey(
        LiabilitiesLoansScenario,
        models.DO_NOTHING,
        db_column="EscenarioId",
        null=True,
        blank=True,
    )
    month = models.IntegerField(
        db_column="Mes", null=True, blank=True, choices=MONTH_CHOICES
    )
    amount_initial = models.DecimalField(
        db_column="MontoInicial",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    percent_growth = models.FloatField(
        db_column="PorcentajeCrecimiento", blank=True, null=True, default=0
    )
    amount_growth = models.DecimalField(
        db_column="MontoCrecimiento",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    principal_payments = models.DecimalField(
        db_column="PagosCapital",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    new_amount = models.DecimalField(
        db_column="MontoTotalCrecimiento",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    rate = models.FloatField(db_column="Tasa", blank=True, null=True, default=0)
    term = models.IntegerField(db_column="Plazo", blank=True, null=True, default=0)
    level_quota = models.DecimalField(
        db_column="CuotaNivelada",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    total_interest = models.DecimalField(
        db_column="InteresesPagados",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )

    comment = models.CharField(
        null=True, blank=True, max_length=500, db_column="Comentario"
    )
    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        related_name="user_upd_liabilities_loans",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPasivoPrestamos"

    def __str__(self):
        return f"{self.month}"
