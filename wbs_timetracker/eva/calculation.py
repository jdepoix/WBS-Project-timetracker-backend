from django.db.transaction import atomic

from core.queryset_cache import QuerysetCache

from data.legacy.project.models import Workpackage, WorkEffort


class EVACalculation(object):
    """
    Handles the recalculation of the earned value analysis values for a given workpackage and all of his parent
    workpackages
    """
    def __init__(self, initial_workpackage):
        self.initial_workpackage = initial_workpackage
        """the workpackage the changes emit from"""

        self.changed_workpackages = [self.initial_workpackage,]
        """holds the workpackages which have been changed"""

        # setup QuerysetCache
        self.workpackage_cache = QuerysetCache(Workpackage.objects.using(self.initial_workpackage._state.db).all())
        self.work_effort_cache = QuerysetCache(WorkEffort.objects.using(self.initial_workpackage._state.db).all())

        # setup attribute maps
        self.workpackage_cache.map_by_attribute('pk')
        self.work_effort_cache.map_by_attribute('workpackage_id')

    def _save_changed_workpackages(self):
        """
        Saves the workpackages which have been changed. This is done in an atomic transaction, to avoid multiple
        requests.
        """
        with atomic():
            for workpackage in self.changed_workpackages:
                workpackage.save()
