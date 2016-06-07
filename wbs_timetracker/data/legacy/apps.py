from django.apps import AppConfig


class LegacyConfig(AppConfig):
    name = 'wbs_timetracker.data.legacy'
    label = 'Legacy'

    def ready(self):
        #TODO load DBs
        pass
