from rest_framework.viewsets import ModelViewSet

from data.legacy.id_wbs.models import DbIdentifier


class ProjectsModelViewSet(ModelViewSet):
    queryset = DbIdentifier.objects.all()
