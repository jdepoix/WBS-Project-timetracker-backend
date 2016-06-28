from rest_framework import viewsets, mixins

from core.api.mixins import EVAUpdateModelMixin

from data.legacy.project.models import Workpackage

from api.workpackages.serializers import WorkpackageSerializer
from api.workpackages.filters import WorkpackageFilter


class WorkpackagesModelViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    EVAUpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    ### Endpoints:

    ```[GET]		/api/projects/<project_id>/workpackages/(?(topleve_wp|inactive))```

        lists all workpackages for the project with the id <project_id>.

        PARAMS:
        - toplevel_wp: <boolean>
            if true only toplevel workpackages are shown, if false only non toplevel workpackages.

        - inactive: <boolean>
            if true only inactive workpackages are shown, if false only active workpackages.

    ```[GET]		/api/projects/<project_id>/workpackages/<workpackage_id>/```

        lists specific information regarding the workpackage with the id <workpackage_id>.

    ```[PATCH]		/api/projects/<project_id>/workpackages/<workpackage_id>/```

        update the ETC of the workpackage with the id <workpackage_id>.

        PATCH DATA:
        {
            /** new etc for this workpackage */
            etc: <double>
        }
    """
    serializer_class = WorkpackageSerializer
    filter_class = WorkpackageFilter

    def get_queryset(self):
        return Workpackage.objects.using(
            self.kwargs.get('project_id')
        ).filter(
            allocated_employees__login=self.request.user.username
        )

    def get_workpackage(self, request, *args, **kwargs):
        return self.get_queryset().get(pk=self.kwargs.get('pk'))
