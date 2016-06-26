from django.db.transaction import atomic

from core.queryset_cache import QuerysetCache

from data.legacy.project.models import Workpackage, WorkEffort


class EVACalculation(object):
    """
    Handles the recalculation of the earned value analysis values for a given workpackage and all of his parent
    workpackages
    """
    def __init__(self, initial_workpackage):
        """
        :param initial_workpackage: the workpackages the changes emit from
        :type initial_workpackage: Workpackage
        """
        self.initial_workpackage = initial_workpackage
        """the workpackage the changes emit from"""

        self.calculated_workpackages = []
        """holds the workpackages which have been changed"""

        # setup QuerysetCache
        self.workpackage_cache = QuerysetCache(Workpackage.objects.using(self.initial_workpackage._state.db).all())
        self.work_effort_cache = QuerysetCache(WorkEffort.objects.using(self.initial_workpackage._state.db).all())

        # setup attribute maps
        self.workpackage_cache.map_by_attribute('id', unique=True)
        self.workpackage_cache.map_by_attribute('parent_id')
        self.work_effort_cache.map_by_attribute('workpackage_id')

    def calculate(self):
        """
        Calculates the EVA values starting with the given initial workpackage and saves the changes
        """
        self._calculate_all_workpackages(self.initial_workpackage)
        self._save_calculated_workpackages()

    def _calculate_all_workpackages(self, initial_workpackage):
        """
        Calculates the given initial workpackage and all direct and indirect parent workpackages

        :param initial_workpackage: the initial workpackage
        :type workpackage: Workpackage
        """
        self._calculate_workpackage(initial_workpackage)

        parent = self.workpackage_cache.id_map.get(initial_workpackage.parent_id)

        if parent:
            self._calculate_all_workpackages(parent)

    def _calculate_unkown_workpackage(self, workpackage):
        """
        Calculates a workpackage without knowing whether it is a toplevel workpackage or not
        :param workpackage: the workpackage to calculate
        :type workpackage: Workpackage
        """
        if workpackage.is_toplevel_wp:
            self._calculate_toplevel_workpackage(workpackage)
        else:
            self._calculate_workpackage(workpackage)

        self.calculated_workpackages.append(workpackage)

    def _calculate_workpackage(self, workpackage):
        """
        Calculates a non toplevel workpackage

        :param workpackage: the workpackage to calculate
        :type workpackage: Workpackage
        """
        pass

    def _calculate_toplevel_workpackage(self, workpackage):
        """
        Calculates a toplevel workpackage

        :param workpackage: the workpackage to calculate
        :type workpackage: Workpackage
        """
        pass

    def _save_calculated_workpackages(self):
        """
        Saves the workpackages which have been calculated. This is done in an atomic transaction, to avoid multiple
        requests.
        """
        with atomic():
            for workpackage in self.calculated_workpackages:
                workpackage.save()

    def _get_workpackage_cached_ac(self, workpackage):
        """
        Returns the AC of a workpackage, calculated using the cached WorkEfforts

        :param workpackage: the workpackage to calculate
        :type workpackage: Workpackage
        :return: workpackages AC
        :rtype: float
        """
        return sum(
            [work_effort.effort for work_effort in self.work_effort_cache.workpackage_id_map.get(workpackage.id)]
        )
