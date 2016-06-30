from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from core.test_utils.factories import TestWBSProjectFactory


class WBSAPITestCase(APITestCase):
    def setUp(self):
        self.project_factory = TestWBSProjectFactory()

        self.client.force_authenticate(user=User.objects.get(username='test_user'))

    def tearDown(self):
        self.project_factory.teardown()
