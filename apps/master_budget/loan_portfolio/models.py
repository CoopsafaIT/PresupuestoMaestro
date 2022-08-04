from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.master_budget.models import MasterParameters
from apps.main.models import Periodo
from utils.constants import MONTH_CHOICES
from apps.master_budget.models import (
    AuditDataMixin, AmountIncreasesMonthlyMixin, AmountDecreasesMonthlyMixin,
    AmountAccountsReceivableMonthlyMixin, MonthlyAdjustmentAmountMixin, CommentMixin,
    CommissionPercentageMonthlyMixin, GrowthPercentageMonthlyMixin,
    PercentageArrearsMonthlyMixin, RateMonthlyMixin, TermMonthlyMixin,
    RecoveryPercentageMonthlyMixin, PercentageInterestDueMonthlyMixin
)


class LoanPortfolioCategory(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    code_core = models.IntegerField(
        db_column="CodigoCategoria", blank=True, null=True
    )
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
        related_name="user_update_loan_portfolio_category",
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroCarteraCredCat"

    def __str__(self):
        return f"{self.name}"


class LoanPortfolioCategoryMap(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    code = models.IntegerField(
        null=True, blank=True, db_column="CodigoPrestamo"
    )
    name = models.CharField(
        null=True, blank=True, max_length=100, db_column="NombrePrestamo"
    )
    category_id = models.ForeignKey(
        LoanPortfolioCategory,
        models.DO_NOTHING,
        db_column="CategoriaId",
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
        null=True,
        blank=True,
        related_name="user_update_loan_portfolio_category_map",
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroCarteraCredCatTipoPrestamos"

    def __str__(self):
        return f"{self.name}"


class LoanPortfolioScenario(
    AuditDataMixin, CommissionPercentageMonthlyMixin,
    GrowthPercentageMonthlyMixin, PercentageArrearsMonthlyMixin,
    RateMonthlyMixin, TermMonthlyMixin, MonthlyAdjustmentAmountMixin,
    RecoveryPercentageMonthlyMixin, PercentageInterestDueMonthlyMixin
):
    id = models.AutoField(primary_key=True, db_column="Id")
    period_id = models.ForeignKey(Periodo, models.DO_NOTHING, db_column="PeriodoId", null=True, blank=True) # NOQA
    parameter_id = models.ForeignKey(MasterParameters, models.DO_NOTHING, db_column="ParametroId")
    category_id = models.ForeignKey(LoanPortfolioCategory, models.DO_NOTHING, db_column="CategoriaId") # NOQA
    correlative = models.CharField(null=True, blank=True, max_length=50, db_column="Correlativo")
    comment = models.CharField(null=True, blank=True, max_length=500, db_column="Comentario")
    is_active = models.BooleanField(null=True, blank=True, default=True, db_column="Estado")
    deleted = models.BooleanField(null=True, blank=True, default=False, db_column="Eliminado")
    base_amount = models.DecimalField(db_column="MontoBase", max_digits=23, decimal_places=2, null=True, blank=True) # NOQA
    annual_growth_percentage = models.FloatField(db_column="PorcentajeCrecimientoAnual", null=True, blank=True) # NOQA
    annual_growth_amount = models.DecimalField(
        db_column="MontoCrecimientoAnual", max_digits=23, decimal_places=2, null=True, blank=True
    )
    created_by = models.ForeignKey(User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True) # NOQA
    updated_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="ActualizadoPor",
        related_name="user_upd_loan_portfolio_scenario", null=True, blank=True
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroCarteraCredEsc"


@receiver(post_save, sender=LoanPortfolioScenario)
def post_save_loan_portfolio(sender, instance, created, **kwargs):
    if created:
        qs = LoanPortfolioScenario.objects.get(pk=instance.pk)
        for item in range(1, 13):
            LoanPortfolio.objects.create(scenario_id=qs, month=item)


class LoanPortfolioComment(CommentMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    scenario_id = models.ForeignKey(
        LoanPortfolioScenario,
        models.DO_NOTHING,
        db_column="EscenarioId",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroCarteraCredMsj"


class LoanPortfolio(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")

    scenario_id = models.ForeignKey(
        LoanPortfolioScenario, models.DO_NOTHING,
        db_column="EscenarioId", null=True, blank=True,
    )
    month = models.IntegerField(
        db_column="Mes", null=True, blank=True, choices=MONTH_CHOICES
    )
    amount_initial = models.DecimalField(
        db_column="MontoInicial", max_digits=23, decimal_places=2,
        blank=True, null=True, default=0
    )
    percent_growth = models.FloatField(
        db_column="PorcentajeCrecimiento", blank=True, null=True, default=0
    )
    amount_growth = models.DecimalField(
        db_column="MontoCrecimiento", max_digits=23, decimal_places=2,
        blank=True, null=True, default=0
    )
    new_amount = models.DecimalField(
        db_column="MontoNuevo", max_digits=23, decimal_places=2,
        blank=True, null=True, default=0
    )
    rate = models.FloatField(db_column="Tasa", blank=True, null=True, default=0)
    term = models.IntegerField(db_column="Plazo", blank=True, null=True, default=0)
    level_quota = models.DecimalField(
        db_column="CuotaNivelada", max_digits=23, decimal_places=2,
        blank=True, null=True, default=0
    )
    total_interest = models.DecimalField(
        db_column="InteresesTotales", max_digits=23, decimal_places=2,
        blank=True, null=True, default=0,
    )
    principal_payments = models.DecimalField(
        db_column="PagosCapital", max_digits=23, decimal_places=2,
        blank=True, null=True, default=0
    )
    percentage_arrears = models.FloatField(
        db_column="PorcentajeMora", blank=True, null=True, default=0
    )
    amount_arrears = models.DecimalField(
        db_column="MontoMora", max_digits=23, decimal_places=2,
        blank=True, null=True, default=0
    )
    default_interest = models.DecimalField(
        db_column="InteresesMoratorios", max_digits=23, decimal_places=2,
        blank=True, null=True, default=0
    )
    commission_percentage = models.FloatField(
        db_column="PorcentajeComision", blank=True, null=True, default=0
    )
    commission_amount = models.DecimalField(
        db_column="MontoComision", max_digits=23, decimal_places=2,
        blank=True, null=True, default=0
    )
    recovery_percentage = models.FloatField(
        db_column="ProcentajeRecuperacion", blank=True, null=True, default=0
    )
    recovery_amount = models.DecimalField(
        db_column="MontoRecuperacion", max_digits=23, decimal_places=2,
        blank=True, null=True, default=0
    )
    percantage_interest_due = models.FloatField(
        db_column="PorcentajeInteresesVencidos", blank=True, null=True, default=0
    )
    interest_due_amount = models.DecimalField(
        db_column="MontoInteresesVencidos", max_digits=23, decimal_places=2,
        blank=True, null=True, default=0
    )
    comment = models.CharField(
        null=True, blank=True, max_length=500, db_column="Comentario"
    )
    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="ActualizadoPor",
        related_name="user_upd_loan_portfolio", null=True, blank=True
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroCarteraCred"

    def __str__(self):
        return f"{self.month}"


class FinancialInvestmentsCategory(AuditDataMixin):
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
        related_name="user_update_financial_investment_category",
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroInversionesFinCat"

    def __str__(self):
        return f"{self.name}"


class FinancialInvestmentsScenario(
    AuditDataMixin,
    AmountIncreasesMonthlyMixin,
    AmountDecreasesMonthlyMixin,
    AmountAccountsReceivableMonthlyMixin,
    RateMonthlyMixin,
):
    id = models.AutoField(primary_key=True, db_column="Id")
    period_id = models.ForeignKey(
        Periodo, models.DO_NOTHING, db_column="PeriodoId", null=True, blank=True
    )
    parameter_id = models.ForeignKey(
        MasterParameters,
        models.DO_NOTHING,
        db_column="ParametroId",
        null=True,
        blank=True,
    )
    category_id = models.ForeignKey(
        FinancialInvestmentsCategory, models.DO_NOTHING, db_column="CategoriaId"
    )
    base_amount = models.DecimalField(
        db_column="MontoBase", max_digits=23, decimal_places=2, null=True, blank=True
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
        related_name="user_upd_financial_investment_scenario",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroInversionesFinEsc"


@receiver(post_save, sender=FinancialInvestmentsScenario)
def post_save_financial_investments(sender, instance, created, **kwargs):
    if created:
        qs = FinancialInvestmentsScenario.objects.get(pk=instance.pk)
        for item in range(1, 13):
            FinancialInvestments.objects.create(scenario_id=qs, month=item)


class FinancialInvestmentsComment(CommentMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    scenario_id = models.ForeignKey(
        FinancialInvestmentsScenario,
        models.DO_NOTHING,
        db_column="EscenarioId",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroInversionesFinMsj"


class FinancialInvestments(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    scenario_id = models.ForeignKey(
        FinancialInvestmentsScenario,
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
    amount_increase = models.DecimalField(
        db_column="MontoAumento",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    amount_decrease = models.DecimalField(
        db_column="MontoDisminucion",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    new_amount = models.DecimalField(
        db_column="MontoNuevo",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    rate = models.FloatField(db_column="Tasa", blank=True, null=True, default=0)
    amount_interest_earned = models.DecimalField(
        db_column="MontoInteresGanado",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    amount_accounts_receivable = models.DecimalField(
        db_column="MontoCuentasPorCobrar",
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
        related_name="user_upd_financial_investment",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroInversionesFin"
