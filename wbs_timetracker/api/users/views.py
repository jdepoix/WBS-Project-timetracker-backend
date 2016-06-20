from rest_framework import mixins, viewsets

from core.api.permissions import IsAuthenticatedOrPostOnly

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
    permission_classes = (IsAuthenticatedOrPostOnly,)
    queryset = WbsUser.objects.all()

    def create(self, request, *args, **kwargs):
        # TODO create user
        pass

    def update(self, request, *args, **kwargs):
        # TODO update user
        pass
