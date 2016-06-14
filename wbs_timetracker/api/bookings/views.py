from core.api.viewsets import EVAModelViewSet

from data.legacy.project.models import WorkEffort

from api.bookings.serializers import WorkEffortSerializer


class BookingsModelViewSet(EVAModelViewSet):
    # TODO filter by workpackage or date
    serializer_class = WorkEffortSerializer

    def get_queryset(self):
        return WorkEffort.objects.using(
            self.kwargs.get('project_id')
        ).filter(
            employee__login=self.request.user.username
        )
