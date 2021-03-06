from rest_framework import mixins, viewsets
from rest_framework.response import Response

from core.api.responses import ExceptionResponse

from data.legacy.project.project_db_loader import ProjectDbLoader

from api.projects.serializers import ProjectsSerializer


class ProjectsModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    ### Endpoints:

    ```[GET]		/api/projects/```

        list all projects for the currently logged in user.

    ```[POST]		/api/projects/```

        this endpoint is called, when a new project is created by the FAT-Client. It doesn't actually create a new project, it is just needed to update the backend, due to crappy legacy code.

        POST DATA:
        no post data is needed, since the information is already in the database.

    ```[GET]		/api/projects/<project_id>/```

        show specific information about the project with the id <project_id>.
    """
    serializer_class = ProjectsSerializer

    def get_queryset(self):
        return self.request.user.wbs_user.projects.all()

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
