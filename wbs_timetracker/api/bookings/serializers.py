from rest_framework import serializers
from rest_framework.exceptions import ParseError

from core.api.serializers import BaseModelSerializer, ZeroTimeDateTimeField

from data.legacy.project.models import WorkEffort, Employees

from api.projects.serializers import SubProjectHyperlinkedRelatedField
from api.workpackages.serializers import WorkpackageSerializer, WorkpackageHyperlinkedRelatedField


class BookingsHyperlinkedRelatedField(SubProjectHyperlinkedRelatedField):
    view_name = 'workeffort-detail'

    @property
    def model(self):
        return WorkEffort


class WorkEffortReadSerializer(BaseModelSerializer):
    self = BookingsHyperlinkedRelatedField(read_only=True, source='*')
    workpackage = WorkpackageSerializer(read_only=True)
    date = ZeroTimeDateTimeField(source='rec_date')
    newETC = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = WorkEffort
        fields = ('effort', 'description', 'date', 'self', 'workpackage', 'newETC',)


class WorkEffortWriteSerializer(WorkEffortReadSerializer):
    workpackage = WorkpackageHyperlinkedRelatedField(write_only=True)

    def create(self, validated_data):
        workpackage = validated_data.get('workpackage')

        if workpackage.is_toplevel_wp:
            raise ParseError('Can\'t book on toplevel workpackage!')

        if (
            not validated_data.get('newETC') and workpackage.etc - validated_data.get('effort') < 0
                or
            validated_data.get('newETC') and validated_data.get('newETC') - validated_data.get('effort') < 0
        ):
            raise ParseError('This booking would bring the ETC below 0, which is not allowed!')

        request = self.context.get('request')

        validated_data['employee'] = Employees.from_request(request)

        if 'newETC' in validated_data:
            validated_data.pop('newETC')

        return self.Meta.model.objects.using(
            request.parser_context.get('kwargs').get('project_id')
        ).create(
            **validated_data
        )
