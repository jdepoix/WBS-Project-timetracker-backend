from rest_framework import mixins, viewsets

from data.wbs_user.models import BookingSession

from api.booking_session.serializers import BookingSessionSerializer, BookingSessionCreateSerializer


class BookingSessionsModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    ```[GET]		booking-sessions/```

        lists the current booking sessions for the currently logged in user

    ```[POST]		booking-sessions/```

        open a new booking session for the currently logged in user.

        POST DATA:
        {
            /** the URL to the workpackage ressource, this is booking is for **/
            workpackage: <URL>
        }

    ```[GET]		booking-sessions/<booking_session_id>/```

        lists the booking session with the id bookings_session_id.

    ```[DELETE]     booking-sessions/<booking_session_id>/```

        closes the current booking session with the id bookings_session_id and creates a corresponding booking
    """
    def get_serializer_class(self):
        if self.action == 'create':
            return BookingSessionCreateSerializer
        else:
            return BookingSessionSerializer

    def get_queryset(self):
        return BookingSession.objects.filter(user=self.request.user.wbs_user)

    def destroy(self, request, *args, **kwargs):
        #TODO implement booking
        pass
