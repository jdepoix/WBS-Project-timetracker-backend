from django.apps import AppConfig


class ProjectConfig(AppConfig):
    name = 'data.legacy.project'
    label = 'Project'

    def ready(self):
        from data.legacy.project.project_db_loader import ProjectDbLoader

        ProjectDbLoader().load_dbs()
