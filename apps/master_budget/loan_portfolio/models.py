from django.db import models
from django.contrib.auth.models import User

from apps.master_budget.models import MasterParameters
from apps.main.models import Periodo


class AuditDataModel(models.Model):
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


class LoanPortfolioCategory(AuditDataModel):
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
        db_table = "pptoMaestroCartCredCategoria"

    def __str__(self):
        return f'{self.name}'


class LoanPortfolioScenario(AuditDataModel):
    id = models.AutoField(primary_key=True, db_column="Id")
    period_id = models.ForeignKey(Periodo, models.DO_NOTHING, db_column="PeriodoId")
    parameter_id = models.ForeignKey(
        MasterParameters, models.DO_NOTHING, db_column="ParametroId"
    )
    category_id = models.ForeignKey(
        LoanPortfolioCategory, models.DO_NOTHING, db_column="CategoriaId"
    )


# class LoanPortfolio(AuditDataModel):
#     id = models.AutoField(primary_key=True, db_column="Id")
#     period_id = models.ForeignKey(Periodo, models.DO_NOTHING, db_column="PeriodoId")
#     parameter_id = models.ForeignKey(
#         MasterParameters, models.DO_NOTHING, db_column="ParametroId"
#     )
#     category_id = models.ForeignKey(
#         LoanPortfolioCategory, models.DO_NOTHING, db_column="CategoriaId"
#     )
#     month = models.CharField(
#         null=True, blank=True, max_length=50, db_column="Mes", choices=MONTH_CHOICES
#     )
#     amount_initial = models.DecimalField(
#         db_column="MontoInicial", max_digits=23, decimal_places=2, blank=True, null=True
#     )
#     percent_growth = models.FloatField(
#         db_column="PorcentajeCrecimiento", blank=True, null=True
#     )
#     amount_growth = models.DecimalField(
#         db_column="MontoCrecimiento",
#         max_digits=23,
#         decimal_places=2,
#         blank=True,
#         null=True
#     )
#     new_amount = models.DecimalField(
#         db_column="MontoNuevo", max_digits=23, decimal_places=2, blank=True, null=True
#     )
#     rate = models.FloatField(db_column="Tasa", blank=True, null=True)
#     term = models.IntegerField(db_column="Plazo", blank=True, null=True)
#     level_quota = models.DecimalField(
#         db_column="CuotaNivelada", max_digits=23, decimal_places=2, blank=True, null=True
#     )
#     total_interest = models.DecimalField(
#         db_column="InteresesTotales",
#         max_digits=23,
#         decimal_places=2,
#         blank=True,
#         null=True
#     )
#     principal_payments = models.DecimalField(
#         db_column="PagosCapital",
#         max_digits=23,
#         decimal_places=2,
#         blank=True,
#         null=True
#     )
#     percentage_arrears = models.FloatField(
#         db_column="PorcentajeMora", blank=True, null=True
#     )
#     amount_arrears = models.DecimalField(
#         db_column="MontoMora",
#         max_digits=23,
#         decimal_places=2,
#         blank=True,
#         null=True
#     )
#     default_interest = models.DecimalField(
#         db_column="InteresesMoratorios",
#         max_digits=23,
#         decimal_places=2,
#         blank=True,
#         null=True
#     )
#     commission_percentage = models.FloatField(
#         db_column="PorcentajeComision", blank=True, null=True
#     )
#     commission_amount = models.DecimalField(
#         db_column="MontoComision",
#         max_digits=23,
#         decimal_places=2,
#         blank=True,
#         null=True
#     )
#     correlative = models.CharField(
#         null=True, blank=True, max_length=50, db_column="Correlativo"
#     )
#     comment = models.CharField(
#         null=True, blank=True, max_length=500, db_column="Comentario"
#     )
#     is_active = models.BooleanField(
#         null=True, blank=True, default=True, db_column="Estado"
#     )
#     created_by = models.ForeignKey(
#         User, models.DO_NOTHING, db_column="CreadoPor"
#     )
#     updated_by = models.ForeignKey(
#         User,
#         models.DO_NOTHING,
#         db_column="ActualizadoPor",
#         related_name="user_upd_loan_portfolio"
#     )

#     class Meta:
#         default_permissions = []
#         db_table = "pptoMaestroCartCred"

#     def __str__(self):
#         return f'{self.name}'
