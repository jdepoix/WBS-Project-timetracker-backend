from rest_framework import serializers

from core.api.serializers import BaseModelSerializer

from data.legacy.project.models import Workpackage

from api.projects.serializers import SubProjectHyperlinkedRelatedField


class WorkpackageHyperlinkedRelatedField(SubProjectHyperlinkedRelatedField):
    view_name = 'workpackage-detail'

    @property
    def model(self):
        return Workpackage


class WorkpackageSerializer(BaseModelSerializer):
    self = WorkpackageHyperlinkedRelatedField(read_only= True, source='*')
    stringId = serializers.CharField(source='string_id', read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

    class Meta:
        model = Workpackage
        fields = ('string_id', 'name', 'description', 'etc', 'self')
