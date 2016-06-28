from rest_framework import mixins, viewsets

from core.api.mixins import EVAUpdateModelMixin, EVADestroyModelMixin

from data.legacy.project.models import WorkEffort

from api.bookings.filters import WorkEffortFilter
from api.bookings.serializers import WorkEffortSerializer


class BookingsModelViewSet(
    mixins.CreateModelMixin,
    EVAUpdateModelMixin,
    EVADestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    ### Endpoints:

    ```[GET]		/api/projects/<project_id>/bookings/(?(date|workpackage_id))```

        lists all bookings on this project.

        PARAMS:
        - date:
            if date is set, only bookings from this date will be listed. Format: YYYY-MM-DD.

        - workpackage_id:
            if workpackage_id is set, only bookings on this workpackage will be listed.

    ```[POST]		/api/projects/<project_id>/bookings/```

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
            description: <String>,
            /** OPTIONAL: the new ETC for the corresponding workpackage. If this isn't set, the ETC will be set to the old ETC - effort */
            newETC: <double>
        }

    ```[GET]		/api/projects/<project_id>/bookings/<booking_id>/```

        lists all information regarding the booking with the booking id <booking_id>.

    ```[PATCH]		/api/projects/<project_id>/bookings/<booking_id>/```

        updates the booking with the id `<booking_id>`. Data format is the same as for POSTs.

    ```[DELETE]	    /api/projects/<project_id>/bookings/<booking_id>/```

        deletes the booking with the id <booking_id>.
    """
    serializer_class = WorkEffortSerializer
    filter_class = WorkEffortFilter

    def get_queryset(self):
        return WorkEffort.objects.using(
            self.kwargs.get('project_id')
        ).filter(
            employee__login=self.request.user.username
        )

    def get_workpackage(self, request, *args, **kwargs):
        return self.get_queryset().get(pk=self.kwargs.get('pk')).workpackage

    def perform_create(self, serializer):
        serializer.save()

        workpackage = serializer.instance.workpackage
        workpackage.etc = serializer.initial_data.get('newETC', workpackage.etc - serializer.instance.effort)

        self.recalc_eva_values(workpackage)
