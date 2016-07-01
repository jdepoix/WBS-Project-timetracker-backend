from rest_framework.reverse import reverse
from rest_framework import status

from core.api.tests.wbs_api_test_case import WBSAPITestCase

from data.legacy.project.models import Workpackage


class WorkpackageModelViewSetTests(WBSAPITestCase):
    def test_list_workpackages(self):
        url = reverse('workpackage-list', kwargs={'project_id': self.project_factory.project_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Workpackage.objects.using(self.project_factory.project_id).count())

    def test_list_workpackages_toplevel_filter(self):
        url = reverse('workpackage-list', kwargs={'project_id': self.project_factory.project_id}) + '?toplevel_wp=true'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            Workpackage.objects.using(self.project_factory.project_id).filter(is_toplevel_wp=True).count()
        )

    def test_update_workpackage(self):
        new_etc = 5

        non_toplevel_workpackage = Workpackage.objects.using(
            self.project_factory.project_id
        ).filter(
            is_toplevel_wp=False
        ).first()

        url = reverse(
            'workpackage-detail',
            kwargs={
                'project_id': self.project_factory.project_id,
                'pk': non_toplevel_workpackage.id
            }
        )

        response = self.client.patch(url, data={
            'etc': new_etc
        })

        non_toplevel_workpackage.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(non_toplevel_workpackage.etc, new_etc)
