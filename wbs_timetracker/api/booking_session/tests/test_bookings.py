from rest_framework import status
from rest_framework.reverse import reverse

from core.api.tests.wbs_api_test_case import WBSAPITestCase

from data.wbs_user.models import BookingSession
from data.legacy.project.models import Workpackage


class BookingSessionsModelViewSetTests(WBSAPITestCase):
    def test_list_booking_session(self):
        url = reverse('bookingsession-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_booking_session(self):
        workpackage = Workpackage.objects.using(self.project_factory.project_id).filter(is_toplevel_wp=False).first()

        url = reverse('bookingsession-list')
        workpackage_url = 'http://localhost' + reverse('workpackage-detail', kwargs={
            'project_id': self.project_factory.project_id,
            'pk': workpackage.id,
        })

        response = self.client.post(url, data={
            'workpackage': workpackage_url
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)

    def test_delete_booking_session(self):
        workpackage = Workpackage.objects.using(self.project_factory.project_id).filter(is_toplevel_wp=False).first()

        session = BookingSession.objects.create(
            db=self.project_factory.db,
            workpackage_id=workpackage.id,
            user=self.project_factory.user.wbs_user
        )

        url = reverse('bookingsession-detail', kwargs={
            'pk': session.id
        })

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BookingSession.objects.filter(user=self.project_factory.user.wbs_user).count(), 0)
