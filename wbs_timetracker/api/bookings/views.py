from rest_framework.viewsets import ModelViewSet

from data.legacy.project.models import WorkEffort

from api.bookings.serializers import WorkEffortSerializer


class BookingsModelViewSet(ModelViewSet):
    serializer_class = WorkEffortSerializer

    def get_queryset(self):
        return WorkEffort.objects.using(
            self.kwargs.get('project_id')
        ).filter(
            employee__login=self.request.user.username
        )

    def create(self, request, *args, **kwargs):
        response = super(BookingsModelViewSet, self).create(request, *args, **kwargs)

        # TODO EVA recalc

        return response

    def update(self, request, *args, **kwargs):
        response = super(BookingsModelViewSet, self).update(request, *args, **kwargs)

        # TODO EVA recalc

        return response

    def destroy(self, request, *args, **kwargs):
        response = super(BookingsModelViewSet, self).destroy(request, *args, **kwargs)

        # TODO EVA recalc

        return response