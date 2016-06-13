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
    isToplevelWp = serializers.BooleanField(source='is_toplevel_wp', read_only=True)
    isInactive = serializers.BooleanField(source='is_inactive', read_only=True)
    bac = serializers.FloatField(read_only=True)
    ac = serializers.FloatField(read_only=True)
    ev = serializers.FloatField(read_only=True)
    eac = serializers.FloatField(read_only=True)
    cpi = serializers.FloatField(read_only=True)

    class Meta:
        model = Workpackage
        fields = (
            'self',
            'stringId',
            'name',
            'description',
            'isToplevelWp',
            'isInactive',
            'etc',
            'bac',
            'ac',
            'ev',
            'eac',
            'cpi',
        )
