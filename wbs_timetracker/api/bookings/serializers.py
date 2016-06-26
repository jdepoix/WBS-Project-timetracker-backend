from rest_framework import serializers
from rest_framework.exceptions import ParseError

from core.api.serializers import BaseModelSerializer, ZeroTimeDateTimeField

from data.legacy.project.models import WorkEffort, Employees

from api.projects.serializers import SubProjectHyperlinkedRelatedField
from api.workpackages.serializers import WorkpackageHyperlinkedRelatedField


class BookingsHyperlinkedRelatedField(SubProjectHyperlinkedRelatedField):
    view_name = 'workeffort-detail'

    @property
    def model(self):
        return WorkEffort


class WorkEffortSerializer(BaseModelSerializer):
    self = BookingsHyperlinkedRelatedField(read_only=True, source='*')
    workpackage = WorkpackageHyperlinkedRelatedField()
    date = ZeroTimeDateTimeField(source='rec_date')
    newETC = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = WorkEffort
        fields = ('effort', 'description', 'date', 'self', 'workpackage', 'newETC',)

    def create(self, validated_data):
        workpackage = validated_data.get('workpackage')

        if workpackage.is_toplevel_wp:
            raise ParseError('Can\'t book on toplevel workpackage!')

        if workpackage.etc - validated_data.get('effort') < 0:
            raise ParseError('This booking would bring the ETC below 0, which is not allowed!')

        request = self.context.get('request')

        validated_data['employee'] = Employees.from_request(request)

        if 'newETC' in validated_data:
            del validated_data['newETC']

        return self.Meta.model.objects.using(
            request.parser_context.get('kwargs').get('project_id')
        ).create(
            **validated_data
        )
