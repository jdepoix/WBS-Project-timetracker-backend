from rest_framework import mixins, viewsets

from core.api.permissions import IsAuthenticatedOrPostOnly

from data.wbs_user.models import WbsUser

from api.users.filters import WbsUserFilter
from api.users.serializers import WbsUserSerializer, WbsUserUpdateSerializer


class WbsUserModelViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    filter_class = WbsUserFilter
    permission_classes = (IsAuthenticatedOrPostOnly,)
    queryset = WbsUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return WbsUserUpdateSerializer
        else:
            return WbsUserSerializer
