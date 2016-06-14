from rest_framework import viewsets, mixins

from core.api.mixins import EVAUpdateModelMixin

from data.legacy.project.models import Workpackage

from api.workpackages.serializers import WorkpackageSerializer


class WorkpackagesModelViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    EVAUpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = WorkpackageSerializer

    def get_queryset(self):
        # TODO filter by logged in user
        return Workpackage.objects.using(
            self.kwargs.get('project_id')
        )
