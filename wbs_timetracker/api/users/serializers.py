from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

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
        if User.objects.filter(username=validated_data.get('user').get('username')).exists():
            raise PermissionDenied(detail='User already exists')

        return User.objects.create_user(
            username=validated_data.get('user').get('username'),
            password=validated_data.get('password')
        ).wbs_user


class WbsUserUpdateSerializer(BaseModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = WbsUser
        fields = ('password',)

    def update(self, instance, validated_data):
       instance.set_password(validated_data.get('password'))
       instance.save()

       return instance.wbs_user


class WbsUserProjectSerializer(BaseModelSerializer):
    db = serializers.CharField(read_only=True)
    project = serializers.HyperlinkedRelatedField(view_name='dbidentifier-detail', write_only=True, queryset=DbIdentifier.objects.all())

    class Meta:
        model = DbIdentifier
        fields = ('self', 'db', 'project',)

    def create(self, validated_data):
        WbsUser.objects.get(
            pk=self.context.get('request').parser_context.get('kwargs').get('user_id')
        ).projects.add(validated_data.get('project'))

        return validated_data.get('project')
