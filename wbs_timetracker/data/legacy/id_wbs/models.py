from django.db import models

from settings.base import CONF


class DbIdentifier(models.Model):
    db = models.CharField(unique=True, max_length=255)

    def __unicode__(self):
        return str(self.db)

    @property
    def db_config(self):
        """
        the db config for this db

        :return: db config dict
        :rtype: dict
        """
        return {
            str(self.id): {
                'ENGINE': CONF.get('database').get('engine'),
                'NAME': self.db,
                'USER': CONF.get('database').get('user'),
                'PASSWORD': CONF.get('database').get('password'),
                'HOST': CONF.get('database').get('host'),
                'PORT': CONF.get('database').get('port'),
            }
        }

    class Meta:
        managed = False
        db_table = 'db_identifier'
