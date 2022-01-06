from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user_id = models.OneToOneField(
        User, models.DO_NOTHING,
        primary_key=True,
        related_name='profile',
        db_column="user_id"
    )
    user_validate_ad = models.BooleanField(
        default=True, blank=True, null=True, db_column="ValidarConAD"
    )

    class Meta:
        db_table = "auth_user_profile"


@receiver(post_save, sender=User)
def user_signals(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user_id=instance)
