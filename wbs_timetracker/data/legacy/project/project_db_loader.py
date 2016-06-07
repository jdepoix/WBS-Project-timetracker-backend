from settings.base import PASSWORDS

from data.core.db_loader import DbLoader
from data.legacy.id_wbs.models import DbIdentifier


class ProjectDbLoader(DbLoader):
    def __init__(self):
        """
        loads the project databases to the runtime environment
        """
        super(ProjectDbLoader, self).__init__(*self._get_project_db_configs())

    def _get_project_db_configs(self):
        """
        :return: list of db configs
        :rtype: list<dict>
        """
        return [self._get_project_db_config(db) for db in DbIdentifier.objects.all()]

    def _get_project_db_config(self, db):
        """
        gets the db config for a given db

        :param db: db to get the config for
        :type db: DbIdentifier
        :return: db config dict
        :rtype: dict
        """
        return {
            str(db.id): {
                'ENGINE': PASSWORDS.get('database').get('engine'),
                'NAME': db.db,
                'USER': PASSWORDS.get('database').get('user'),
                'PASSWORD': PASSWORDS.get('database').get('password'),
                'HOST': PASSWORDS.get('database').get('host'),
                'PORT': PASSWORDS.get('database').get('port'),
            }
        }
