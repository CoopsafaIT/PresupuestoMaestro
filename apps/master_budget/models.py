from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.main.models import Periodo
from utils.constants import (
    STATUS,
    TYPE_COMPLEMENTARY_PROJECTION,
    MONTH_CHOICES,
    SURPLUS_DISTRIBUTION_CRITERIA,
)


class CommentMixin(models.Model):
    id = models.AutoField(primary_key=True, db_column="Id")
    comment = models.CharField(
        null=True, blank=True, max_length=500, db_column="Comentario"
    )
    deleted = models.BooleanField(
        null=True, blank=True, default=True, db_column="Borrado"
    )
    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    created_at = models.DateTimeField(
        db_column="FechaCreacion", blank=True, null=True, auto_now_add=True
    )

    class Meta:
        abstract = True


class GrowthPercentageMonthlyMixin(models.Model):
    growth_percentage_january = models.FloatField(
        db_column="PorcentajeCrecimientoEne", null=True, blank=True, default=0
    )
    growth_percentage_february = models.FloatField(
        db_column="PorcentajeCrecimientoFeb", null=True, blank=True, default=0
    )
    growth_percentage_march = models.FloatField(
        db_column="PorcentajeCrecimientoMar", null=True, blank=True, default=0
    )
    growth_percentage_april = models.FloatField(
        db_column="PorcentajeCrecimientoAbr", null=True, blank=True, default=0
    )
    growth_percentage_may = models.FloatField(
        db_column="PorcentajeCrecimientoMay", null=True, blank=True, default=0
    )
    growth_percentage_june = models.FloatField(
        db_column="PorcentajeCrecimientoJun", null=True, blank=True, default=0
    )
    growth_percentage_july = models.FloatField(
        db_column="PorcentajeCrecimientoJul", null=True, blank=True, default=0
    )
    growth_percentage_august = models.FloatField(
        db_column="PorcentajeCrecimientoAgo", null=True, blank=True, default=0
    )
    growth_percentage_september = models.FloatField(
        db_column="PorcentajeCrecimientoSep", null=True, blank=True, default=0
    )
    growth_percentage_october = models.FloatField(
        db_column="PorcentajeCrecimientoOct", null=True, blank=True, default=0
    )
    growth_percentage_november = models.FloatField(
        db_column="PorcentajeCrecimientoNov", null=True, blank=True, default=0
    )
    growth_percentage_december = models.FloatField(
        db_column="PorcentajeCrecimientoDic", null=True, blank=True, default=0
    )

    class Meta:
        abstract = True


class PercentageArrearsMonthlyMixin(models.Model):
    percentage_arrears_january = models.FloatField(
        db_column="PorcentajeMoraEne", null=True, blank=True, default=0
    )
    percentage_arrears_february = models.FloatField(
        db_column="PorcentajeMoraFeb", null=True, blank=True, default=0
    )
    percentage_arrears_march = models.FloatField(
        db_column="PorcentajeMoraMar", null=True, blank=True, default=0
    )
    percentage_arrears_april = models.FloatField(
        db_column="PorcentajeMoraAbr", null=True, blank=True, default=0
    )
    percentage_arrears_may = models.FloatField(
        db_column="PorcentajeMoraMay", null=True, blank=True, default=0
    )
    percentage_arrears_june = models.FloatField(
        db_column="PorcentajeMoraJun", null=True, blank=True, default=0
    )
    percentage_arrears_july = models.FloatField(
        db_column="PorcentajeMoraJul", null=True, blank=True, default=0
    )
    percentage_arrears_august = models.FloatField(
        db_column="PorcentajeMoraAgo", null=True, blank=True, default=0
    )
    percentage_arrears_september = models.FloatField(
        db_column="PorcentajeMoraSep", null=True, blank=True, default=0
    )
    percentage_arrears_october = models.FloatField(
        db_column="PorcentajeMoraOct", null=True, blank=True, default=0
    )
    percentage_arrears_november = models.FloatField(
        db_column="PorcentajeMoraNov", null=True, blank=True, default=0
    )
    percentage_arrears_december = models.FloatField(
        db_column="PorcentajeMoraDic", null=True, blank=True, default=0
    )

    class Meta:
        abstract = True


class CommissionPercentageMonthlyMixin(models.Model):
    commission_percentage_january = models.FloatField(
        db_column="PorcentajeComisionEne", null=True, blank=True, default=0
    )
    commission_percentage_february = models.FloatField(
        db_column="PorcentajeComisionFeb", null=True, blank=True, default=0
    )
    commission_percentage_march = models.FloatField(
        db_column="PorcentajeComisionMar", null=True, blank=True, default=0
    )
    commission_percentage_april = models.FloatField(
        db_column="PorcentajeComisionAbr", null=True, blank=True, default=0
    )
    commission_percentage_may = models.FloatField(
        db_column="PorcentajeComisionMay", null=True, blank=True, default=0
    )
    commission_percentage_june = models.FloatField(
        db_column="PorcentajeComisionJun", null=True, blank=True, default=0
    )
    commission_percentage_july = models.FloatField(
        db_column="PorcentajeComisionJul", null=True, blank=True, default=0
    )
    commission_percentage_august = models.FloatField(
        db_column="PorcentajeComisionAgo", null=True, blank=True, default=0
    )
    commission_percentage_september = models.FloatField(
        db_column="PorcentajeComisionSep", null=True, blank=True, default=0
    )
    commission_percentage_october = models.FloatField(
        db_column="PorcentajeComisionOct", null=True, blank=True, default=0
    )
    commission_percentage_november = models.FloatField(
        db_column="PorcentajeComisionNov", null=True, blank=True, default=0
    )
    commission_percentage_december = models.FloatField(
        db_column="PorcentajeComisionDic", null=True, blank=True, default=0
    )

    class Meta:
        abstract = True


class RateMonthlyMixin(models.Model):
    rate_january = models.FloatField(
        db_column="TasaEne", null=True, blank=True, default=0
    )
    rate_february = models.FloatField(
        db_column="TasaFeb", null=True, blank=True, default=0
    )
    rate_march = models.FloatField(
        db_column="TasaMar", null=True, blank=True, default=0
    )
    rate_april = models.FloatField(
        db_column="TasaAbr", null=True, blank=True, default=0
    )
    rate_may = models.FloatField(
        db_column="TasaMay", null=True, blank=True, default=0
    )
    rate_june = models.FloatField(
        db_column="TasaJun", null=True, blank=True, default=0
    )
    rate_july = models.FloatField(
        db_column="TasaJul", null=True, blank=True, default=0
    )
    rate_august = models.FloatField(
        db_column="TasaAgo", null=True, blank=True, default=0
    )
    rate_september = models.FloatField(
        db_column="TasaSep", null=True, blank=True, default=0
    )
    rate_october = models.FloatField(
        db_column="TasaOct", null=True, blank=True, default=0
    )
    rate_november = models.FloatField(
        db_column="TasaNov", null=True, blank=True, default=0
    )
    rate_december = models.FloatField(
        db_column="TasaDic", null=True, blank=True, default=0
    )

    class Meta:
        abstract = True


class TermMonthlyMixin(models.Model):
    term_january = models.FloatField(
        db_column="PlazoEne", null=True, blank=True, default=0,
    )
    term_february = models.FloatField(
        db_column="PlazoFeb", null=True, blank=True, default=0,
    )
    term_march = models.FloatField(
        db_column="PlazoMar", null=True, blank=True, default=0,
    )
    term_april = models.FloatField(
        db_column="PlazoAbr", null=True, blank=True, default=0,
    )
    term_may = models.FloatField(
        db_column="PlazoMay", null=True, blank=True, default=0,
    )
    term_june = models.FloatField(
        db_column="PlazoJun", null=True, blank=True, default=0,
    )
    term_july = models.FloatField(
        db_column="PlazoJul", null=True, blank=True, default=0,
    )
    term_august = models.FloatField(
        db_column="PlazoAgo", null=True, blank=True, default=0,
    )
    term_september = models.FloatField(
        db_column="PlazoSep", null=True, blank=True, default=0,
    )
    term_october = models.FloatField(
        db_column="PlazoOct", null=True, blank=True, default=0,
    )
    term_november = models.FloatField(
        db_column="PlazoNov", null=True, blank=True, default=0,
    )
    term_december = models.FloatField(
        db_column="PlazoDic", null=True, blank=True, default=0,
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


class AmountIncreasesMonthlyMixin(models.Model):
    increases_january = models.DecimalField(
        db_column="AumentoEne",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    increases_february = models.DecimalField(
        db_column="AumentoFeb",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    increases_march = models.DecimalField(
        db_column="AumentoMar",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    increases_april = models.DecimalField(
        db_column="AumentoAbr",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    increases_may = models.DecimalField(
        db_column="AumentoMay",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    increases_june = models.DecimalField(
        db_column="AumentoJun",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    increases_july = models.DecimalField(
        db_column="AumentoJul",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    increases_august = models.DecimalField(
        db_column="AumentoAgo",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    increases_september = models.DecimalField(
        db_column="AumentoSep",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    increases_october = models.DecimalField(
        db_column="AumentoOct",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    increases_november = models.DecimalField(
        db_column="AumentoNov",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    increases_december = models.DecimalField(
        db_column="AumentoDic",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )

    class Meta:
        abstract = True


class AmountDecreasesMonthlyMixin(models.Model):
    decreases_january = models.DecimalField(
        db_column="DisminucionesEne",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    decreases_february = models.DecimalField(
        db_column="DisminucionesFeb",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    decreases_march = models.DecimalField(
        db_column="DisminucionesMar",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    decreases_april = models.DecimalField(
        db_column="DisminucionesAbr",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    decreases_may = models.DecimalField(
        db_column="DisminucionesMay",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    decreases_june = models.DecimalField(
        db_column="DisminucionesJun",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    decreases_july = models.DecimalField(
        db_column="DisminucionesJul",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    decreases_august = models.DecimalField(
        db_column="DisminucionesAgo",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    decreases_september = models.DecimalField(
        db_column="DisminucionesSep",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    decreases_october = models.DecimalField(
        db_column="DisminucionesOct",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    decreases_november = models.DecimalField(
        db_column="DisminucionesNov",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    decreases_december = models.DecimalField(
        db_column="DisminucionesDic",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )

    class Meta:
        abstract = True


class AmountAccountsReceivableMonthlyMixin(models.Model):
    amount_accounts_receivable_january = models.DecimalField(
        db_column="CuentasXCobrarEne",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_accounts_receivable_february = models.DecimalField(
        db_column="CuentasXCobrarFeb",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_accounts_receivable_march = models.DecimalField(
        db_column="CuentasXCobrarMar",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_accounts_receivable_april = models.DecimalField(
        db_column="CuentasXCobrarAbr",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_accounts_receivable_may = models.DecimalField(
        db_column="CuentasXCobrarsMay",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_accounts_receivable_june = models.DecimalField(
        db_column="CuentasXCobrarJun",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_accounts_receivable_july = models.DecimalField(
        db_column="CuentasXCobrarJul",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_accounts_receivable_august = models.DecimalField(
        db_column="CuentasXCobrarAgo",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_accounts_receivable_september = models.DecimalField(
        db_column="CuentasXCobrarSep",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_accounts_receivable_october = models.DecimalField(
        db_column="CuentasXCobrarOct",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_accounts_receivable_november = models.DecimalField(
        db_column="CuentasXCobrarNov",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_accounts_receivable_december = models.DecimalField(
        db_column="CuentasXCobrarDic",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )

    class Meta:
        abstract = True


class PercentageIncreasesMonthlyMixin(models.Model):
    percentage_increase_january = models.FloatField(
        db_column="PorcentajeincrementoEne", null=True, blank=True, default=0
    )
    percentage_increase_february = models.FloatField(
        db_column="PorcentajeincrementoFeb", null=True, blank=True, default=0
    )
    percentage_increase_march = models.FloatField(
        db_column="PorcentajeincrementoMar", null=True, blank=True, default=0
    )
    percentage_increase_april = models.FloatField(
        db_column="PorcentajeincrementoAbr", null=True, blank=True, default=0
    )
    percentage_increase_may = models.FloatField(
        db_column="PorcentajeincrementoMay", null=True, blank=True, default=0
    )
    percentage_increase_june = models.FloatField(
        db_column="PorcentajeincrementoJun", null=True, blank=True, default=0
    )
    percentage_increase_july = models.FloatField(
        db_column="PorcentajeincrementoJul", null=True, blank=True, default=0
    )
    percentage_increase_august = models.FloatField(
        db_column="PorcentajeincrementoAgo", null=True, blank=True, default=0
    )
    percentage_increase_september = models.FloatField(
        db_column="PorcentajeincrementoSep", null=True, blank=True, default=0
    )
    percentage_increase_october = models.FloatField(
        db_column="PorcentajeincrementoOct", null=True, blank=True, default=0
    )
    percentage_increase_november = models.FloatField(
        db_column="PorcentajeincrementoNov", null=True, blank=True, default=0
    )
    percentage_increase_december = models.FloatField(
        db_column="PorcentajeincrementoDic", null=True, blank=True, default=0
    )

    class Meta:
        abstract = True


class AmountMonthlyMixin(models.Model):
    amount_january = models.DecimalField(
        db_column="MontoEne",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_february = models.DecimalField(
        db_column="MontoFeb",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_march = models.DecimalField(
        db_column="MontoMar",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_april = models.DecimalField(
        db_column="MontoAbr",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_may = models.DecimalField(
        db_column="MontoMay",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_june = models.DecimalField(
        db_column="MontoJun",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_july = models.DecimalField(
        db_column="MontoJul",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_august = models.DecimalField(
        db_column="MontoAgo",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_september = models.DecimalField(
        db_column="MontoSep",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_october = models.DecimalField(
        db_column="MontoOct",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_november = models.DecimalField(
        db_column="MontoNov",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_december = models.DecimalField(
        db_column="MontoDic",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )

    class Meta:
        abstract = True


class AmountMonthlyMixinTemporal(models.Model):
    amount_temp_january = models.DecimalField(
        db_column="MontoTemporalEne",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_temp_february = models.DecimalField(
        db_column="MontoTemporalFeb",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_temp_march = models.DecimalField(
        db_column="MontoTemporalMar",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_temp_april = models.DecimalField(
        db_column="MontoTemporalAbr",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_temp_may = models.DecimalField(
        db_column="MontoTemporalMay",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_temp_june = models.DecimalField(
        db_column="MontoTemporalJun",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_temp_july = models.DecimalField(
        db_column="MontoTemporalJul",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_temp_august = models.DecimalField(
        db_column="MontoTemporalAgo",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_temp_september = models.DecimalField(
        db_column="MontoTemporalSep",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_temp_october = models.DecimalField(
        db_column="MontoTemporalOct",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_temp_november = models.DecimalField(
        db_column="MontoTemporalNov",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )
    amount_temp_december = models.DecimalField(
        db_column="MontoTemporalDic",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )

    class Meta:
        abstract = True


class MasterParameters(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    date_base = models.DateField(null=True, blank=True, db_column="FechaBase")
    period_id = models.ForeignKey(Periodo, models.DO_NOTHING, db_column="PeriodoId")
    is_active = models.BooleanField(
        null=True, blank=True, default=False, db_column="Estado", choices=STATUS
    )
    deleted = models.BooleanField(
        null=True, blank=True, default=False, db_column="Eliminado"
    )
    comment = models.CharField(
        null=True, blank=True, max_length=200, db_column="Comentario"
    )
    name = models.CharField(
        null=True, blank=True, max_length=50, db_column="Nombre"
    )
    correlative = models.CharField(
        null=True, blank=True, max_length=50, db_column="Correlativo"
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
        related_name="user_update_parameter"
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroParametros"
        ordering = ("period_id", "-date_base",)

    def __str__(self):
        return self.date_base.strftime("%d/%m/%Y")


@receiver(post_save, sender=MasterParameters)
def post_save_master_parameters(sender, instance, created, **kwargs):
    catalog_list = CatalogLossesEarnings.objects.all()
    for catalog in catalog_list:
        for month in range(1, 13):
            if not LossesEarningsComplementaryProjection.objects.filter(
                category_id=catalog.pk, period_id=instance.period_id.pk, month=month
            ).exists():
                LossesEarningsComplementaryProjection.objects.create(
                    category_id=catalog, period_id=instance.period_id, month=month
                )


class CatalogLossesEarnings(models.Model):
    id = models.AutoField(primary_key=True, db_column="Id")
    type = models.CharField(
        db_column="Tipo", max_length=1, null=True,
        blank=True, choices=TYPE_COMPLEMENTARY_PROJECTION
    )
    method = models.CharField(
        db_column="Metodo", max_length=1, null=True, blank=True
    )
    level_one = models.CharField(
        null=True, blank=True, max_length=200, db_column="Nivel1"
    )
    level_two = models.CharField(
        null=True, blank=True, max_length=200, db_column="Nivel2"
    )
    level_three = models.CharField(
        null=True, blank=True, max_length=200, db_column="Nivel3"
    )
    level_four = models.CharField(
        null=True, blank=True, max_length=200, db_column="Nivel4"
    )
    order = models.IntegerField(
        null=True, blank=True, db_column="Orden"
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPerdidasGananciasCatalogo"
        ordering = ("type", "order", )


class LossesEarningsComplementaryProjection(models.Model):
    id = models.AutoField(primary_key=True, db_column="Id")
    period_id = models.ForeignKey(
        Periodo, models.DO_NOTHING, null=True, blank=True, db_column="PeriodoId"
    )
    category_id = models.ForeignKey(
        CatalogLossesEarnings, models.DO_NOTHING, db_column="CategoriaId"
    )
    month = models.IntegerField(
        null=True, blank=True, db_column="Mes", choices=MONTH_CHOICES
    )
    amount = models.DecimalField(
        db_column="Saldo",
        null=True,
        blank=True,
        max_digits=23,
        decimal_places=2,
        default=0
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroPerdidasGananciasProyeccionComplementaria"
        ordering = ("category_id", "-month",)


class SurplusDistributionCategory(models.Model):
    """Model definition for SurplusDistribution."""
    id = models.AutoField(primary_key=True, db_column="Id")

    class Meta:
        """Meta definition for SurplusDistribution."""
        default_permissions = []
        db_table = "pptoMaestroDistribucionExcedentesCategoria"


class SurplusDistribution(models.Model):
    """Model definition for SurplusDistribution."""
    id = models.AutoField(primary_key=True, db_column="Id")
    # period_id = models.ForeignKey(
    #     Periodo, models.DO_NOTHING, null=True, blank=True, db_column="PeriodoId"
    # )
    # title = models.CharField(db_column="Titulo", null=True, blank=True, max_length=50)
    # criteria = models.CharField(
    #     db_column="Criterio",
    #     null=True,
    #     blank=True,
    #     choices=SURPLUS_DISTRIBUTION_CRITERIA
    # )
    # percentage = models.FloatField(
    #     db_column="Porcentaje", null=True, blank=True, default=0
    # )
    # value = models.DecimalField(
    #     db_column="Valor",
    #     null=True,
    #     blank=True,
    #     max_digits=23,
    #     decimal_places=2,
    #     default=0
    # )
    # type = ''


    class Meta:
        """Meta definition for SurplusDistribution."""
        default_permissions = []
        db_table = "pptoMaestroDistribucionExcedentes"
