from rest_framework import mixins, viewsets

from data.wbs_user.models import WbsUser

from api.users.filters import WbsUserFilter
from api.users.serializers import WbsUserSerializer


class WbsUserModelViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = WbsUserSerializer
    filter_class = WbsUserFilter
    queryset = WbsUser.objects.all()
