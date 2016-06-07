from django.apps import AppConfig


class ProjectConfig(AppConfig):
    name = 'wbs_timetracker.data.legacy.project'
    label = 'Project'

    def ready(self):
        #TODO load DBs
        pass
