from django.db import models

from settings.base import PASSWORDS


class DbIdentifier(models.Model):
    db = models.CharField(unique=True, max_length=255)

    @property
    def db_config(self):
        """
        the db config for this db

        :return: db config dict
        :rtype: dict
        """
        return {
            str(self.id): {
                'ENGINE': PASSWORDS.get('database').get('engine'),
                'NAME': self.db,
                'USER': PASSWORDS.get('database').get('user'),
                'PASSWORD': PASSWORDS.get('database').get('password'),
                'HOST': PASSWORDS.get('database').get('host'),
                'PORT': PASSWORDS.get('database').get('port'),
            }
        }

    class Meta:
        managed = False
        db_table = 'db_identifier'
