from django.db import models
from django.contrib.auth.models import User

from apps.master_budget.models import MasterParameters
from apps.main.models import Periodo
from utils.constants import MONTH_CHOICES


class GrowthPercentageMonthlyMixin(models.Model):
    growth_percentage_january = models.FloatField(
        db_column="PorcentajeCrecimientoEne", null=True, blank=True
    )
    growth_percentage_february = models.FloatField(
        db_column="PorcentajeCrecimientoFeb", null=True, blank=True
    )
    growth_percentage_march = models.FloatField(
        db_column="PorcentajeCrecimientoMar", null=True, blank=True
    )
    growth_percentage_april = models.FloatField(
        db_column="PorcentajeCrecimientoAbr", null=True, blank=True
    )
    growth_percentage_may = models.FloatField(
        db_column="PorcentajeCrecimientoMay", null=True, blank=True
    )
    growth_percentage_june = models.FloatField(
        db_column="PorcentajeCrecimientoJun", null=True, blank=True
    )
    growth_percentage_july = models.FloatField(
        db_column="PorcentajeCrecimientoJul", null=True, blank=True
    )
    growth_percentage_august = models.FloatField(
        db_column="PorcentajeCrecimientoAgo", null=True, blank=True
    )
    growth_percentage_september = models.FloatField(
        db_column="PorcentajeCrecimientoSep", null=True, blank=True
    )
    growth_percentage_october = models.FloatField(
        db_column="PorcentajeCrecimientoOct", null=True, blank=True
    )
    growth_percentage_november = models.FloatField(
        db_column="PorcentajeCrecimientoNov", null=True, blank=True
    )
    growth_percentage_december = models.FloatField(
        db_column="PorcentajeCrecimientoDic", null=True, blank=True
    )

    class Meta:
        abstract = True


class PercentageArrearsMonthlyMixin(models.Model):
    percentage_arrears_january = models.FloatField(
        db_column="PorcentajeMoraEne", null=True, blank=True
    )
    percentage_arrears_february = models.FloatField(
        db_column="PorcentajeMoraFeb", null=True, blank=True
    )
    percentage_arrears_march = models.FloatField(
        db_column="PorcentajeMoraMar", null=True, blank=True
    )
    percentage_arrears_april = models.FloatField(
        db_column="PorcentajeMoraAbr", null=True, blank=True
    )
    percentage_arrears_may = models.FloatField(
        db_column="PorcentajeMoraMay", null=True, blank=True
    )
    percentage_arrears_june = models.FloatField(
        db_column="PorcentajeMoraJun", null=True, blank=True
    )
    percentage_arrears_july = models.FloatField(
        db_column="PorcentajeMoraJul", null=True, blank=True
    )
    percentage_arrears_august = models.FloatField(
        db_column="PorcentajeMoraAgo", null=True, blank=True
    )
    percentage_arrears_september = models.FloatField(
        db_column="PorcentajeMoraSep", null=True, blank=True
    )
    percentage_arrears_october = models.FloatField(
        db_column="PorcentajeMoraOct", null=True, blank=True
    )
    percentage_arrears_november = models.FloatField(
        db_column="PorcentajeMoraNov", null=True, blank=True
    )
    percentage_arrears_december = models.FloatField(
        db_column="PorcentajeMoraDic", null=True, blank=True
    )

    class Meta:
        abstract = True


class CommissionPercentageMonthlyMixin(models.Model):
    commission_percentage_january = models.FloatField(
        db_column="PorcentajeComisionEne", null=True, blank=True
    )
    commission_percentage_february = models.FloatField(
        db_column="PorcentajeComisionFeb", null=True, blank=True
    )
    commission_percentage_march = models.FloatField(
        db_column="PorcentajeComisionMar", null=True, blank=True
    )
    commission_percentage_april = models.FloatField(
        db_column="PorcentajeComisionAbr", null=True, blank=True
    )
    commission_percentage_may = models.FloatField(
        db_column="PorcentajeComisionMay", null=True, blank=True
    )
    commission_percentage_june = models.FloatField(
        db_column="PorcentajeComisionJun", null=True, blank=True
    )
    commission_percentage_july = models.FloatField(
        db_column="PorcentajeComisionJul", null=True, blank=True
    )
    commission_percentage_august = models.FloatField(
        db_column="PorcentajeComisionAgo", null=True, blank=True
    )
    commission_percentage_september = models.FloatField(
        db_column="PorcentajeComisionSep", null=True, blank=True
    )
    commission_percentage_october = models.FloatField(
        db_column="PorcentajeComisionOct", null=True, blank=True
    )
    commission_percentage_november = models.FloatField(
        db_column="PorcentajeComisionNov", null=True, blank=True
    )
    commission_percentage_december = models.FloatField(
        db_column="PorcentajeComisionDic", null=True, blank=True
    )

    class Meta:
        abstract = True


class RateMonthlyMixin(models.Model):
    rate_january = models.FloatField(
        db_column="TasaEne", null=True, blank=True
    )
    rate_february = models.FloatField(
        db_column="TasaFeb", null=True, blank=True
    )
    rate_march = models.FloatField(
        db_column="TasaMar", null=True, blank=True
    )
    rate_april = models.FloatField(
        db_column="TasaAbr", null=True, blank=True
    )
    rate_may = models.FloatField(
        db_column="TasaMay", null=True, blank=True
    )
    rate_june = models.FloatField(
        db_column="TasaJun", null=True, blank=True
    )
    rate_july = models.FloatField(
        db_column="TasaJul", null=True, blank=True
    )
    rate_august = models.FloatField(
        db_column="TasaAgo", null=True, blank=True
    )
    rate_september = models.FloatField(
        db_column="TasaSep", null=True, blank=True
    )
    rate_october = models.FloatField(
        db_column="TasaOct", null=True, blank=True
    )
    rate_november = models.FloatField(
        db_column="TasaNov", null=True, blank=True
    )
    rate_december = models.FloatField(
        db_column="TasaDic", null=True, blank=True
    )

    class Meta:
        abstract = True


class TermMonthlyMixin(models.Model):
    term_january = models.FloatField(
        db_column="TermEne", null=True, blank=True
    )
    term_february = models.FloatField(
        db_column="TermFeb", null=True, blank=True
    )
    term_march = models.FloatField(
        db_column="TermMar", null=True, blank=True
    )
    term_april = models.FloatField(
        db_column="TermAbr", null=True, blank=True
    )
    term_may = models.FloatField(
        db_column="TermMay", null=True, blank=True
    )
    term_june = models.FloatField(
        db_column="TermJun", null=True, blank=True
    )
    term_july = models.FloatField(
        db_column="TermJul", null=True, blank=True
    )
    term_august = models.FloatField(
        db_column="TermAgo", null=True, blank=True
    )
    term_september = models.FloatField(
        db_column="TermSep", null=True, blank=True
    )
    term_october = models.FloatField(
        db_column="TermOct", null=True, blank=True
    )
    term_november = models.FloatField(
        db_column="TermNov", null=True, blank=True
    )
    term_december = models.FloatField(
        db_column="TermDic", null=True, blank=True
    )

    class Meta:
        abstract = True


class AuditDataMixin(models.Model):
    """Model definition for AuditDataModel."""
    created_at = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True, auto_now_add=True
    )
    updated_at = models.DateTimeField(
        db_column="FechaActualizacion", blank=True, null=True, auto_now=True
    )

    class Meta:
        """Meta definition for AuditDataModel."""
        abstract = True


class LoanPortfolioCategory(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    name = models.CharField(
        null=True, blank=True, max_length=50, db_column="Nombre"
    )
    is_active = models.BooleanField(
        null=True, blank=True, default=True, db_column="Estado"
    )
    identifier = models.CharField(
        null=True, blank=True, max_length=50, db_column="Identificador"
    )
    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor"
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        related_name="user_update_loan_portfolio_category"
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroCarteraCredCat"

    def __str__(self):
        return f'{self.name}'


class LoanPortfolioScenario(
    AuditDataMixin,
    CommissionPercentageMonthlyMixin,
    GrowthPercentageMonthlyMixin,
    PercentageArrearsMonthlyMixin,
    RateMonthlyMixin,
    TermMonthlyMixin,
):
    id = models.AutoField(primary_key=True, db_column="Id")
    period_id = models.ForeignKey(Periodo, models.DO_NOTHING, db_column="PeriodoId")
    parameter_id = models.ForeignKey(
        MasterParameters, models.DO_NOTHING, db_column="ParametroId"
    )
    category_id = models.ForeignKey(
        LoanPortfolioCategory, models.DO_NOTHING, db_column="CategoriaId"
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
    base_amount = models.DecimalField(
        db_column="MontoBase", max_digits=23, decimal_places=2, null=True, blank=True
    )
    annual_growth_percentage = models.FloatField(
        db_column="PorcentajeCrecimientoAnual", null=True, blank=True
    )
    annual_growth_amount = models.DecimalField(
        db_column="MontoCrecimientoAnual",
        max_digits=23,
        decimal_places=2,
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        related_name="user_upd_loan_portfolio_scenario",
        null=True,
        blank=True
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroCarteraCredEsc"


class LoanPortfolio(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")

    scenario_id = models.ForeignKey(
        LoanPortfolioScenario,
        models.DO_NOTHING,
        db_column="EscenarioId",
        null=True,
        blank=True
    )
    month = models.IntegerField(
        db_column="Mes", null=True, blank=True, choices=MONTH_CHOICES
    )
    amount_initial = models.DecimalField(
        db_column="MontoInicial", max_digits=23, decimal_places=2, blank=True, null=True
    )
    percent_growth = models.FloatField(
        db_column="PorcentajeCrecimiento", blank=True, null=True
    )
    amount_growth = models.DecimalField(
        db_column="MontoCrecimiento",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True
    )
    new_amount = models.DecimalField(
        db_column="MontoNuevo", max_digits=23, decimal_places=2, blank=True, null=True
    )
    rate = models.FloatField(db_column="Tasa", blank=True, null=True)
    term = models.IntegerField(db_column="Plazo", blank=True, null=True)
    level_quota = models.DecimalField(
        db_column="CuotaNivelada", max_digits=23, decimal_places=2, blank=True, null=True
    )
    total_interest = models.DecimalField(
        db_column="InteresesTotales",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True
    )
    principal_payments = models.DecimalField(
        db_column="PagosCapital",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True
    )
    percentage_arrears = models.FloatField(
        db_column="PorcentajeMora", blank=True, null=True
    )
    amount_arrears = models.DecimalField(
        db_column="MontoMora",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True
    )
    default_interest = models.DecimalField(
        db_column="InteresesMoratorios",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True
    )
    commission_percentage = models.FloatField(
        db_column="PorcentajeComision", blank=True, null=True
    )
    commission_amount = models.DecimalField(
        db_column="MontoComision",
        max_digits=23,
        decimal_places=2,
        blank=True,
        null=True
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
    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        related_name="user_upd_loan_portfolio",
        null=True,
        blank=True
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroCarteraCred"

    def __str__(self):
        return f'{self.name}'
