from rest_framework import serializers

from core.api.serializers import BaseModelSerializer, ZeroTimeDateTimeField

from data.legacy.project.models import WorkEffort

from api.projects.serializers import SubProjectHyperlinkedRelatedField


class BookingsHyperlinkedRelatedField(SubProjectHyperlinkedRelatedField):
    view_name = 'workeffort-detail'

    @property
    def model(self):
        return WorkEffort


class WorkEffortSerializer(BaseModelSerializer):
    #TODO add link to workpackage
    self = BookingsHyperlinkedRelatedField(read_only=True, source='*')
    date = ZeroTimeDateTimeField(source='rec_date')

    class Meta:
        model = WorkEffort
        fields = ['effort', 'description', 'date', 'self']
