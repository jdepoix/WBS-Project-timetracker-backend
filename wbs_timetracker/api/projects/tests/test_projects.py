from core.api.tests.wbs_api_test_case import WBSAPITestCase

from rest_framework.reverse import reverse
from rest_framework import status


class ProjectModelViewSetTests(WBSAPITestCase):
    def test_list_projects(self):
        url = reverse('dbidentifier-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.project_factory.user.wbs_user.projects.count())
