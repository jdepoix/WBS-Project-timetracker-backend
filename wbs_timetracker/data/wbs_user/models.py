from django.contrib.auth.models import User
from django.db import models

from data.legacy.id_wbs.models import DbIdentifier


class WbsUser(models.Model):
    user = models.OneToOneField(User, related_name='wbs_user', on_delete=models.CASCADE)
    projects = models.ManyToManyField(DbIdentifier, related_name='wbs_users')
    start_current_booking_session = models.DateTimeField(null=True, default=None)
