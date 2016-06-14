from core.api.serializers import BaseModelSerializer, ZeroTimeDateTimeField

from data.legacy.project.models import WorkEffort

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
        # TODO implement create porperly
        pass