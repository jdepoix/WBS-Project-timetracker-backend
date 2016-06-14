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

    class Meta:
        model = WorkEffort
        fields = ('effort', 'description', 'date', 'self', 'workpackage',)

    def create(self, validated_data):
        request = self.context.get('request')

        validated_data['employee'] = Employees.from_request(request)

        return self.Meta.model.objects.using(
            request.parser_context.get('kwargs').get('project_id')
        ).create(
            **validated_data
        )
