from core.api.viewsets import EVAModelViewSet

from data.legacy.project.models import WorkEffort

from api.bookings.serializers import WorkEffortSerializer


class BookingsModelViewSet(EVAModelViewSet):
    """
    ### Endpoints:

    ```[GET]		projects/<project_id>/bookings/(?(date|workpackage_id))```

        lists all bookings on this project.

        PARAMS:
        - date:
            if date is set, only bookings from this date will be listed.

        - workpackage_id:
            if workpackage_id is set, only bookings on this workpackage will be listed.

    ```[POST]		projects/<project_id>/bookings/```

        creates a new booking.

        POST DATA:
        {
            /** link to the workpackage this booking belongs to */
            workpackage: <URL>,
            /** the date of this booking. Format: YYYY-MM-DD */
            date: <date>,
            /** the workeffort in workdays (8h) */
            effort: <double>,
            /** the description of what was done */
            description: <String>
        }

    ```[GET]		projects/<project_id>/bookings/<booking_id>/```

        lists all information regarding the booking with the booking id <booking_id>.

    ```[PATCH]		projects/<project_id>/bookings/<booking_id>/```

        updates the booking with the id `<booking_id>`. Data format is the same as for POSTs.

    ```[DELETE]	    projects/<project_id>/bookings/<booking_id>/```

        deletes the booking with the id <booking_id>.
    """
    # TODO filter by workpackage or date
    serializer_class = WorkEffortSerializer

    def get_queryset(self):
        return WorkEffort.objects.using(
            self.kwargs.get('project_id')
        ).filter(
            employee__login=self.request.user.username
        )
