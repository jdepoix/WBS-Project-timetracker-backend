from rest_framework import viewsets, mixins

from data.legacy.project.models import Workpackage

from api.workpackages.serializers import WorkpackageSerializer


class WorkpackagesModelViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = WorkpackageSerializer

    def get_queryset(self):
        # TODO
        # return Workpackage.objects.using(
        #     self.kwargs.get('project_id')
        # ).filter(
        #     employee__login=self.request.user.username
        # )
        pass


    def update(self, request, *args, **kwargs):
        response = super(WorkpackagesModelViewSet, self).update(request, *args, **kwargs)

        # TODO EVA recalc

        return response
