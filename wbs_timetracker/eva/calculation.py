from django.db.transaction import atomic

from core.queryset_cache import QuerysetCache

from data.legacy.project.models import Workpackage, WorkEffort, Employees

class CalculatabelWorkpackage(object):
    """
    Wraps a Workpackage and adds additional functionality needed to calculate the earned value analysis values
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

        self._calculate_cpi()

    def _calculate_workpackage(self):
        """
        Calculates a non toplevel workpackage
        """
        self._calculate_etc_costs()
        self._calculate_cached_ac()
        self._calculate_cached_ac_costs()
        self._calculate_eac()
        self._calculate_ev()

    def _calculate_toplevel_workpackage(self):
        """
        Calculates a toplevel workpackage
        """
        # TODO implement
        pass

    def _get_completion_status(self):
        """
        Returns the completion status percentage.

        :return: completion status, ranging from 0 to 1
        :rtype: float
        """
        return self.workpackage.ac / self.workpackage.eac

    def _calculate_cached_ac(self):
        """
        Calculates the AC of the workpackage, calculated using the cached WorkEfforts of the given CalculationManager
        """
        self.workpackage.ac = sum(
            [
                work_effort.effort
                    for work_effort in self._get_work_efforts()
            ]
        )

    def _calculate_cached_ac_costs(self):
        """
        Calculates the AC costs of the workpackage, using cached WorkEfforts
        """
        ac_costs = 0.

        for work_effort in self._get_work_efforts():
            employee = self._get_employee_by_work_effort(work_effort)

            if employee:
                ac_costs += work_effort.effort * employee.daily_rate

        self.workpackage.ac_costs = ac_costs

    def _calculate_etc_costs(self):
        """
        Calculates the ETC costs
        """
        self.workpackage.etc_costs = self.workpackage.etc * self.workpackage.wp_daily_rate

    def _calculate_eac(self):
        """
        Calculates the EAC
        """
        self.workpackage.eac = self.workpackage.etc_costs + self.workpackage.ac_costs

    def _calculate_ev(self):
        """
        Calculates the EV
        """
        self.workpackage.ev = self.workpackage.bac_costs * self._get_completion_status()

    def _calculate_cpi(self):
        """
        Calculates the CPI
        """
        # NOTE:     this seems wrong, but it is the way the CPI is calculated in the FAT client. Therefore it has to be
        #           done the same way, to stay consistent...
        if self.workpackage.eac == 0. and self.workpackage.bac_costs == 0.:
            cpi = 1.
        else:
            cpi = self.workpackage.bac_costs / self.workpackage.eac

        if cpi > 10.:
            cpi = 10.

        self.workpackage.cpi = cpi

    def _get_work_efforts(self):
        """
        Returns the WorkEfforts for this workpackage from the cached WorkEfforts

        :rtype: list<WorkEffort>
        """
        return self.calculation_manager.get_work_efforts_by_workpackage(self.workpackage)

    def _get_employee_by_work_effort(self, work_effort):
        """
        Returns a employee who did make the given WorkEffort

        :param work_effort: the WorkEffort the Employee should be returned for
        :type work_effort: WorkEffort
        :return: the employee belonging to the given WorkEffort
        :rtype: Employees
        """
        return self.calculation_manager.get_employee_by_work_effort(work_effort)


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

        project_id = self.initial_workpackage._state.db

        # setup QuerysetCache
        self.workpackage_cache = QuerysetCache(Workpackage.objects.using(project_id).all())
        self.work_effort_cache = QuerysetCache(WorkEffort.objects.using(project_id).all())
        self.employee_cache = QuerysetCache(Employees.objects.using(project_id).all())

        # setup attribute maps
        self.workpackage_cache.map_by_attribute('id', unique=True)
        self.workpackage_cache.map_by_attribute('parent_id')
        self.work_effort_cache.map_by_attribute('workpackage_id')
        self.employee_cache.map_by_attribute('id', unique=True)

    def get_work_efforts_by_workpackage(self, workpackage):
        """
        Returns the WorkEfforts for a workpackage from the cached WorkEfforts

        :param workpackage: the workpackage the WorkEfforts should be returned for
        :return: list of WorkEfforts
        :rtype: list<WorkEffort>
        """
        return self.work_effort_cache.workpackage_id_map.get(workpackage.id)

    def get_employee_by_work_effort(self, work_effort):
        """
        Returns a employee who did make the given WorkEffort

        :param work_effort: the WorkEffort the Employee should be returned for
        :type work_effort: WorkEffort
        :return: the employee belonging to the given WorkEffort
        :rtype: Employees
        """
        return self.employee_cache.id_map.get(work_effort.employee.id)

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
