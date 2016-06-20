from django.contrib.auth.models import User

from rest_framework import serializers

from core.api.serializers import BaseModelSerializer

from data.legacy.id_wbs.models import DbIdentifier
from data.wbs_user.models import WbsUser


class WbsUserSerializer(BaseModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(write_only=True)
    projects = BaseModelSerializer.default_serializer_factory(DbIdentifier)(many=True, read_only=True)

    class Meta:
        model = WbsUser
        fields = ('self', 'username', 'projects', 'password',)

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data.get('user').get('username'),
            password=validated_data.get('password')
        ).wbs_user
