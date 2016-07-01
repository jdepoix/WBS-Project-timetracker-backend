from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from data.legacy.id_wbs.models import DbIdentifier
from data.legacy.project.models import Workpackage


class BookingSession(models.Model):
    """
    Represents a single booking session for a specific user. Each user can only have one booking session at a time
    """
    # since workpackages are stored in a different DB, a ForeignKey can't be used here
    workpackage_id = models.IntegerField()
    db = models.ForeignKey(DbIdentifier)
    user = models.OneToOneField('WbsUser', related_name='booking_session', on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField(auto_now_add=True)

    @property
    def workpackage(self):
        return Workpackage.objects.using(str(self.db.id)).get(pk=self.workpackage_id)


class WbsUser(models.Model):
    """
    extends the django user model and adds relations to the projects the given user is participating in
    """
    user = models.OneToOneField(User, related_name='wbs_user', on_delete=models.CASCADE)
    projects = models.ManyToManyField(DbIdentifier, related_name='wbs_users')

    def __unicode__(self):
        return self.user.username

    @staticmethod
    def create_wbs_user(sender, instance, created, **kwargs):
        if created:
            WbsUser.objects.get_or_create(user=instance)


post_save.connect(WbsUser.create_wbs_user, sender=User)
