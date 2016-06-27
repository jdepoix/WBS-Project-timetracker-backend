from django.db.transaction import atomic

from core.queryset_cache import QuerysetCache

from data.legacy.project.models import Workpackage, WorkEffort


class CalculatabelWorkpackage(object):
    """
    wraps a workpackage and adds additional functionality needed to calculate the earned value analysis values
    """
    def __init__(self, workpackage, calculation_manager):
        """
        :param workpackage: the workpackage which should be wrapped
        :type workpackage: Workpackage
        :param calculation_manager: the supervisoring calculation manager which is used for caching
        :type calculation_manager: EVACalculationManager
        """
        self.workpackage = workpackage
        self.calculation_manager = calculation_manager

    def calculate(self):
        """
        Calculates the workpackage without knowing whether it is a toplevel workpackage or not
        """
        if self.workpackage.is_toplevel_wp:
            self._calculate_toplevel_workpackage()
        else:
            self._calculate_workpackage()

    def _calculate_workpackage(self):
        """
        Calculates a non toplevel workpackage
        """
        # TODO implement
        pass

    def _calculate_toplevel_workpackage(self):
        """
        Calculates a toplevel workpackage
        """
        # TODO implement
        pass

    def _calculate_cached_ac(self):
        """
        Calculated the AC of the workpackage, calculated using the cached WorkEfforts of the given CalculationManager
        """
        self.ac = sum(
            [
                work_effort.effort
                    for work_effort in self.calculation_manager.get_work_efforts_by_workpackage(self.workpackage)
            ]
        )

    def _calculate_cached_ac_cost(self):
        """
        calculates the AC costs of the workpackage, using cached WorkEfforts
        """
        pass


class EVACalculationManager(object):
    """
    Handles the recalculation of the earned value analysis values for a given workpackage and all of his parent
    workpackages, using caching to improve performance
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

    def get_work_efforts_by_workpackage(self, workpackage):
        """
        returns the WorkEfforts for a workpackage from the cached WorkEfforts

        :param workpackage: the workpackage the WorkEfforts should be returned for
        :return: list of WorkEfforts
        :rtype: list<WorkEffort>
        """
        return self.work_effort_cache.workpackage_id_map.get(workpackage.id)

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
        CalculatabelWorkpackage(initial_workpackage).calculate()
        self.calculated_workpackages.append(initial_workpackage)

        parent = self.workpackage_cache.id_map.get(initial_workpackage.parent_id)

        if parent:
            self._calculate_all_workpackages(parent)

    def _save_calculated_workpackages(self):
        """
        Saves the workpackages which have been calculated. This is done in an atomic transaction, to avoid multiple
        requests.
        """
        with atomic():
            for workpackage in self.calculated_workpackages:
                workpackage.save()
