from data.legacy.id_wbs.models import DbIdentifier
from rest_framework import serializers

from core.api.serializers import BaseModelSerializer

from data.wbs_user.models import WbsUser


class WbsUserSerializer(BaseModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(write_only=True)
    projects = BaseModelSerializer.default_serializer_factory(DbIdentifier)(many=True, read_only=True)

    class Meta:
        model = WbsUser
        fields = ('self', 'username', 'projects', 'password',)
