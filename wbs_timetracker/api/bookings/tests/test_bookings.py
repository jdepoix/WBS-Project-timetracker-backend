import datetime

from rest_framework import status
from rest_framework.reverse import reverse

from core.api.tests.wbs_api_test_case import WBSAPITestCase

from data.legacy.project.models import WorkEffort, Workpackage


class BookingsModelViewSetTests(WBSAPITestCase):
    def test_list_bookings(self):
        url = reverse('workeffort-list', kwargs={
            'project_id': self.project_factory.project_id
        })

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            WorkEffort.objects.using(
                self.project_factory.project_id
            ).filter(
                employee__login=self.project_factory.user.username
            ).count()
        )

    def test_list_bookings_workpackage_filter(self):
        workpackage = Workpackage.objects.using(self.project_factory.project_id).filter(is_toplevel_wp=False).first()

        url = reverse('workeffort-list', kwargs={
            'project_id': self.project_factory.project_id
        }) + '?workpackage_id=' + str(workpackage.id)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            WorkEffort.objects.using(
                self.project_factory.project_id
            ).filter(
                employee__login=self.project_factory.user.username,
                workpackage=workpackage
            ).count()
        )

    def test_create_booking(self):
        url = reverse('workeffort-list', kwargs={
            'project_id': self.project_factory.project_id
        })

        old_work_effort_count = WorkEffort.objects.all().using(self.project_factory.project_id).count()

        workpackage = Workpackage.objects.using(self.project_factory.project_id).filter(is_toplevel_wp=False).first()
        effort = 1
        date = str(datetime.datetime.now().date())
        description = 'description'

        workpackage_url = reverse('workpackage-detail', kwargs={
            'project_id': self.project_factory.project_id,
            'pk': workpackage.id
        })

        response = self.client.post(url, data={
            'date': date,
            'effort': effort,
            'workpackage': workpackage_url,
            'description': description,
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            WorkEffort.objects.all().using(self.project_factory.project_id).count(),
            old_work_effort_count + 1
        )

        updated_workpackage = Workpackage.objects.using(self.project_factory.project_id).get(pk=workpackage.id)

        self.assertEqual(updated_workpackage.etc, workpackage.etc - effort)

    def test_update_booking(self):
        work_effort = WorkEffort.objects.using(self.project_factory.project_id).first()

        url = reverse('workeffort-detail', kwargs={
            'project_id': self.project_factory.project_id,
            'pk': work_effort.id
        })

        new_description = 'new fancy description'

        response = self.client.patch(url, data={
            'description': new_description
        })

        work_effort.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(work_effort.description, new_description)

    def test_delete_booking(self):
        work_effort = WorkEffort.objects.using(self.project_factory.project_id).first()

        url = reverse('workeffort-detail', kwargs={
            'project_id': self.project_factory.project_id,
            'pk': work_effort.id
        })

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertRaises(
            WorkEffort.DoesNotExist,
            lambda: WorkEffort.objects.using(self.project_factory.project_id).get(pk=work_effort.id)
        )
