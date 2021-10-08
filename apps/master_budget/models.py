from django.db import models
from django.contrib.auth.models import User

from apps.main.models import Periodo
# from utils.constants import MONTH_CHOICES


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


class MasterParameters(AuditDataModel):
    id = models.AutoField(primary_key=True, db_column="Id")
    date_base = models.DateField(null=True, blank=True, db_column="FechaBase")
    period_id = models.ForeignKey(Periodo, models.DO_NOTHING, db_column="PeriodoId")
    is_active = models.BooleanField(
        null=True, blank=True, default=False, db_column="Estado"
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
        User, models.DO_NOTHING, db_column="CreadoPor"
    )
    updated_by = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="ActualizadoPor",
        related_name="user_update_parameter"
    )

    class Meta:
        default_permissions = []
        db_table = "pptoMaestroParametros"
        ordering = ("name",)
