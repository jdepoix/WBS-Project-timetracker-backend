from rest_framework import mixins, viewsets


class BookingSessionsModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    ```[GET]		booking-session/```

        lists the current booking sessions for the currently logged in user

    ```[POST]		booking-session/```

        open a new booking session for the currently logged in user.

        POST DATA:
        {
            /** the URL to the workpackage ressource, this is booking is for **/
            workpackage: <URL>
        }

    ```[GET]		booking-session/<booking_session_id>/```

        lists the booking session with the id bookings_session_id.

    ```[DELETE]     booking-session/<booking_session_id>/```

        closes the current booking session with the id bookings_session_id and creates a corresponding booking
    """
    pass
