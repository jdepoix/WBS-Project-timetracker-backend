from rest_framework import serializers

from core.api.serializers import BaseModelSerializer, ZeroTimeDateTimeField

from data.legacy.project.models import WorkEffort


class WorkEffortSerializer(BaseModelSerializer):
    #TODO add link to workpackage
    #TODO custom self link
    # self = serializers.HyperlinkedIdentityField(view_name='workeffort-detail')
    date = ZeroTimeDateTimeField(source='rec_date')

    class Meta:
        model = WorkEffort
        fields = ['effort', 'description', 'date']
