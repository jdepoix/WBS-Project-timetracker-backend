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
    """
    ### Endpoints:

    ```[GET]		projects/<project_id>/workpackages/```

        lists all workpackages for the project with the id <project_id>.

    ```[GET]		projects/<project_id>/workpackages/<workpackage_id>/```

        lists specific information regarding the workpackage with the id <workpackage_id>.

    ```[PATCH]		projects/<project_id>/workpackages/<workpackage_id>/```

        update the ETC of the workpackage with the id <workpackage_id>.

        PATCH DATA:
        {
            /** new etc for this workpackage */
            etc: <double>
        }
    """
    # TODO implement and document filtering by inactive and toplevel
    serializer_class = WorkpackageSerializer

    def get_queryset(self):
        return Workpackage.objects.using(
            self.kwargs.get('project_id')
        ).filter(
            allocated_employees__login=self.request.user.username
        )
