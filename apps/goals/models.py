from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.db.models.constraints import UniqueConstraint

from apps.main.models import Periodo, Centroscosto
from apps.master_budget.models import (
    AuditDataMixin, AmountMonthlyMixin, AmountMonthlyExecutionMixin
)
from utils.constants import TYPE_GOALS, DEFINITION_EXECUTION_GOALS


class GlobalGoalPeriod(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    description = models.CharField(
        null=True, blank=True, max_length=500, db_column="Descripcion"
    )
    period_id = models.OneToOneField(
        Periodo, models.DO_NOTHING, null=True, blank=True, db_column="PeriodoId"
    )
    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        related_name="user_update_global_goal_period",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "MetasGlobalPeriodo"


@receiver(post_save, sender=Periodo)
def post_save_period(sender, instance, created, **kwargs):
    qs = instance
    global_goal_period = GlobalGoalPeriod.objects.filter(period_id=qs.pk).first()
    if not global_goal_period:
        GlobalGoalPeriod.objects.create(
            period_id=qs, description='Creado desde el sistema'
        )


class Goal(AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    description = models.CharField(
        null=True, blank=True, max_length=500, db_column="Descripcion"
    )
    type = models.CharField(
        default='M',
        db_column="Tipo", max_length=1, null=True,
        blank=True, choices=TYPE_GOALS
    )
    query = models.CharField(
        null=True, blank=True, max_length=300, db_column="SQLQuery"
    )
    definition = models.CharField(
        default='M',
        null=True,
        blank=True,
        max_length=1,
        db_column="Definicion",
        choices=DEFINITION_EXECUTION_GOALS
    )
    execution = models.CharField(
        default='M',
        null=True,
        blank=True,
        max_length=1,
        db_column="Ejecucion",
        choices=DEFINITION_EXECUTION_GOALS
    )
    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        related_name="user_update_goal",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "Metas"

    def __str__(self):
        return f'{self.description}'


class GlobalGoalDetail(AmountMonthlyMixin, AuditDataMixin):
    id = models.AutoField(primary_key=True, db_column="Id")
    id_global_goal_period = models.ForeignKey(
        GlobalGoalPeriod, models.DO_NOTHING, null=True, db_column="IdMetasGlobalesPeriodo"
    )
    id_goal = models.ForeignKey(
        Goal, models.DO_NOTHING, null=True, db_column="IdMetas"
    )
    annual_amount = models.DecimalField(
        db_column="MontoAnual", null=True, blank=True,
        max_digits=23, decimal_places=2, default=0
    )
    ponderation = models.FloatField(
        db_column="Ponderacion",
        null=True,
        blank=True,
        default=0
    )

    percentage = models.FloatField(
        db_column="Porcentaje",
        null=True,
        blank=True,
        default=0
    )

    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )

    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        related_name="user_update_global_goal_detail",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "MetasGlobalDetalle"
        unique_together = ('id_global_goal_period', 'id_goal')


@receiver(post_save, sender=GlobalGoalDetail)
def post_save_global_goal(sender, instance, created, **kwargs):
    if created:
        cecos = Centroscosto.objects.filter(habilitado=True).exclude(
            agencia__in=['1', '0001', '9000']
        )
        for item in cecos:
            SubsidiaryGoalDetail.objects.create(
                id_cost_center=item, id_global_goal_detail=instance,
                id_global_goal_period=instance.id_global_goal_period,
                id_goal=instance.id_goal, annual_amount_subsidiary=0,
                ponderation=instance.ponderation
            )


class SubsidiaryGoalDetail(AmountMonthlyMixin, AmountMonthlyExecutionMixin, AuditDataMixin): # NOQA
    id = models.AutoField(primary_key=True, db_column="Id")
    id_global_goal_period = models.ForeignKey(
        GlobalGoalPeriod, models.DO_NOTHING, null=True, db_column="IdMetasGlobalesPeriodo"
    )
    id_global_goal_detail = models.ForeignKey(
        GlobalGoalDetail, models.DO_NOTHING, null=True, db_column="IdMetaGlobal"
    )
    id_goal = models.ForeignKey(
        Goal, models.DO_NOTHING, null=True, db_column="IdMetas"
    )
    id_cost_center = models.ForeignKey(
        Centroscosto, models.DO_NOTHING, null=True, db_column="IdFilial"
    )
    annual_amount_subsidiary = models.DecimalField(
        db_column="MontoAnualFilial", null=True, blank=True,
        max_digits=23, decimal_places=2, default=0
    )

    ponderation = models.FloatField(
        db_column="Ponderacion",
        null=True,
        blank=True,
        default=0
    )
    percentage = models.FloatField(
        db_column="Porcentaje",
        null=True,
        blank=True,
        default=0
    )

    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="CreadoPor", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        related_name="user_update_subsidiary_goal_detail",
        null=True,
        blank=True,
    )

    class Meta:
        default_permissions = []
        db_table = "MetasFilialDetalle"
        unique_together = ('id_global_goal_period', 'id_goal', 'id_cost_center')
