from django.db import models


class DbIdentifier(models.Model):
    db = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'db_identifier'
