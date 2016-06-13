from rest_framework import viewsets, mixins

from data.legacy.project.models import Workpackage

from api.workpackages.serializers import WorkpackageSerializer


class WorkpackagesModelViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = WorkpackageSerializer

    def get_queryset(self):
        # TODO filter by logged in user
        return Workpackage.objects.using(
            self.kwargs.get('project_id')
        )

    def update(self, request, *args, **kwargs):
        response = super(WorkpackagesModelViewSet, self).update(request, *args, **kwargs)

        # TODO EVA recalc

        return response
