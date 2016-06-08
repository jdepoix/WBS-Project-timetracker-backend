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
        return [db.db_config for db in DbIdentifier.objects.all()]
