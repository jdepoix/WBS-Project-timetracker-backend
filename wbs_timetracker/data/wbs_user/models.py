from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from data.legacy.id_wbs.models import DbIdentifier


class WbsUser(models.Model):
    user = models.OneToOneField(User, related_name='wbs_user', on_delete=models.CASCADE)
    projects = models.ManyToManyField(DbIdentifier, related_name='wbs_users')
    # TODO rework booking model
    start_current_booking_session = models.DateTimeField(null=True, default=None)

    @staticmethod
    def create_wbs_user(sender, instance, created, **kwargs):
        if created:
            WbsUser.objects.get_or_create(user=instance)


post_save.connect(WbsUser.create_wbs_user, sender=User)
