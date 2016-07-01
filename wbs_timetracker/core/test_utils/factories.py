from django.utils import timezone
from django.contrib.auth.models import User

from data.legacy.project.project_db_loader import ProjectDbLoader
from data.legacy.id_wbs.models import *
from data.legacy.project.models import *
from data.wbs_user.models import BookingSession


class TestWBSProjectFactory(object):
    """
    creates a WBS Project used for tests
    """
    def __init__(self):
        self.create_user()
        self.create_test_wbs_project()
        self.create_employee()
        self.create_workpackages()
        self.create_work_efforts()

    def create_test_wbs_project(self):
        self.db = DbIdentifier.objects.create(
            db='test_project'
        )
        self.project_id = str(self.db.id)
        ProjectDbLoader().load_dbs()

        self.user.wbs_user.projects.add(self.db)

    def create_employee(self):
        self.employee = Employees.objects.using(self.project_id).create(
            login='test_user',
            last_name='user',
            first_name='test',
            project_leader=1,
            daily_rate=1,
            time_preference=0,
        )

    def create_workpackage(self, **kwargs):
        return Workpackage.objects.using(self.project_id).create(
            string_id=kwargs.get('string_id'),
            fid_project=1,
            resp_employee=self.employee,
            parent_id=kwargs.get('parent_id'),
            parent_order_id=kwargs.get('parent_order_id'),
            name=kwargs.get('name'),
            description='',
            bac=kwargs.get('bac'),
            ac=0,
            ev=0,
            etc=kwargs.get('bac'),
            eac=kwargs.get('bac'),
            cpi=0,
            bac_costs=kwargs.get('bac'),
            ac_costs=0,
            etc_costs=kwargs.get('bac'),
            wp_daily_rate=1,
            release_date=timezone.now(),
            is_toplevel_wp=kwargs.get('is_toplevel_wp'),
            is_inactive=0,
            start_date_calc=timezone.now(),
            start_date_wish=timezone.now(),
            end_date_calc=timezone.now(),
        )

    def create_workpackages(self):
        self.workpackages = []

        parent_workpackage = self.create_workpackage(
            string_id='1.0',
            parent_id=0,
            parent_order_id=1,
            name='test_project',
            bac=20,
            is_toplevel_wp=1,
        )

        self.workpackages.append(
            parent_workpackage
        )

        self.workpackages.append(
            self.create_workpackage(
                string_id='1.1',
                parent_id=parent_workpackage.id,
                parent_order_id=1,
                name='ap1',
                bac=10,
                is_toplevel_wp=0,
            )
        )

        self.workpackages.append(
            self.create_workpackage(
                string_id='1.2',
                parent_id=parent_workpackage.id,
                parent_order_id=2,
                name='ap2',
                bac=10,
                is_toplevel_wp=0,
            )
        )

        for workpackage in self.workpackages:
            WpAllocation.objects.using(self.project_id).create(
                workpackage=workpackage,
                employee=self.employee,
            )

    def create_user(self):
        self.user = User.objects.create_user(username='test_user', password='test')

    def create_work_efforts(self):
        workpackages = Workpackage.objects.using(self.project_id).filter(is_toplevel_wp=False)
        self.work_efforts = []

        for workpackage in workpackages:
            self.work_efforts.append(
                WorkEffort.objects.using(self.project_id).create(
                    workpackage=workpackage,
                    employee=self.employee,
                    rec_date=timezone.now(),
                    effort=0,
                    description='none',
                )
            )

    def teardown(self):
        WorkEffort.objects.using(self.project_id).delete()
        BookingSession.objects.all().delete()
        User.objects.all().delete()
        WpAllocation.objects.using(self.project_id).delete()
        Workpackage.objects.using(self.project_id).delete()
        Employees.objects.using(self.project_id).delete()
