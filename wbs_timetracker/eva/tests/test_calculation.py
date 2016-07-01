from core.api.tests.wbs_api_test_case import WBSAPITestCase

from data.legacy.project.models import Workpackage

from eva.calculation import EVACalculationManager


class EVACalculationTests(WBSAPITestCase):
    def test_eva_calculation(self):
        old_workpackage = Workpackage.objects.using(
            self.project_factory.project_id
        ).filter(
            is_toplevel_wp=False
        ).first()

        old_parent_workpackage = Workpackage.objects.using(
            self.project_factory.project_id
        ).get(
            pk=old_workpackage.parent_id
        )

        etc_reduction = 5

        old_workpackage.etc -= etc_reduction

        EVACalculationManager(old_workpackage).calculate()

        new_workpackage = Workpackage.objects.using(self.project_factory.project_id).get(pk=old_workpackage.id)
        new_parent_workpackage = Workpackage.objects.using(
            self.project_factory.project_id
        ).get(
            pk=old_parent_workpackage.id
        )

        self.assertEqual(new_workpackage.etc, old_workpackage.etc)
        self.assertEqual(new_parent_workpackage.etc, old_parent_workpackage.etc - etc_reduction)
