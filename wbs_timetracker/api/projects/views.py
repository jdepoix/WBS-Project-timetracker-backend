from rest_framework import mixins, viewsets
from rest_framework.response import Response

from core.api.serializers import BaseModelSerializer
from core.api.responses import ExceptionResponse

from data.legacy.project.project_db_loader import ProjectDbLoader
from data.legacy.id_wbs.models import DbIdentifier


class ProjectsModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    ### Endpoints:

    ```[GET]		projects/```

        list all projects for the currently logged in user.

    ```[POST]		projects/```

        this endpoint is called, when a new project is created by the FAT-Client. It doesn't actually create a new project, it is just needed to update the backend, due to crappy legacy code.

        POST DATA:
        no post data is needed, since the information is already in the database.

    ```[GET]		projects/<project_id>/```

        show specific information about the project with the id <project_id>.
    """
    queryset = DbIdentifier.objects.all()
    serializer_class = BaseModelSerializer.default_serializer_factory(DbIdentifier)

    def create(self, request, *args, **kwargs):
        """
        reloads the Projects databases from the DbIdentifier table

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            ProjectDbLoader().load_dbs()
            return Response(
                status=201
            )
        except Exception as e:
            return ExceptionResponse(exception=e)
