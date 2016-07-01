from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.reverse import reverse

from core.api.tests.wbs_api_test_case import WBSAPITestCase

from data.wbs_user.models import WbsUser


class UsersModelViewSetTests(WBSAPITestCase):
    def test_list_users(self):
        url = reverse('wbsuser-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), WbsUser.objects.all().count())

    def test_create_user(self):
        new_user_name = 'new_user'
        new_password = 'new_password'

        url = reverse('wbsuser-list')

        response = self.client.post(url, data={
            'username': new_user_name,
            'password': new_password
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_user = User.objects.get(username=new_user_name)

        self.assertIsNot(None, new_user)
        self.assertIsNot(None, new_user.wbs_user)
        self.assertTrue(new_user.check_password(new_password))

    def test_change_password(self):
        new_password = 'new_fancy_password'

        url = reverse('wbsuser-detail', kwargs={'pk': self.project_factory.user.wbs_user.id})

        response = self.client.patch(url, data={
            'password': new_password
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_user_projects(self):
        url = reverse('userprojects-list', kwargs={'user_id': self.project_factory.user.wbs_user.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.project_factory.user.wbs_user.projects.all().count())
