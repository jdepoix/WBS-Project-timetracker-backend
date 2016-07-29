from rest_framework import serializers
from rest_framework.exceptions import NotFound, ParseError

from core.api.urlresolvers import URLString
from core.api.serializers import BaseModelSerializer

from data.legacy.id_wbs.models import DbIdentifier
from data.legacy.project.models import Workpackage
from data.wbs_user.models import BookingSession

from api.workpackages.serializers import WorkpackageSerializer


class BookingSessionSerializer(BaseModelSerializer):
    startTime = serializers.DateTimeField(read_only=True, format='%Y-%m-%dT%H:%M:%S', source='start_time')
    workpackage = serializers.SerializerMethodField()

    def get_workpackage(self, obj):
        request = self.context.get('request')
        request.parser_context.get('kwargs')['project_id'] = obj.db.id
        return WorkpackageSerializer(obj.workpackage, context={'request': request}).data

    class Meta:
        model = BookingSession
        fields = ('workpackage', 'self', 'startTime')


class BookingSessionCreateSerializer(BookingSessionSerializer):
    """
    only handel's creating booking sessions
    """
    workpackage = serializers.URLField(write_only=True)

    def create(self, validated_data):
        kwargs = URLString(validated_data.get('workpackage')).resolve().kwargs

        try:
            project_id = kwargs['project_id']

            project = DbIdentifier.objects.get(pk=project_id)
            workpackage = Workpackage.objects.using(project_id).get(pk=kwargs['pk'])
        except (Workpackage.DoesNotExist, DbIdentifier.DoesNotExist, KeyError):
            raise NotFound('Workpackage wasn\'t found!')

        if workpackage.is_toplevel_wp:
            raise ParseError('Booking on toplevel workpackages is not allowed!')

        user = self.context.get('request').user.wbs_user

        if hasattr(user, 'booking_session'):
            raise ParseError(
                'There already is an open booking session for this user. ' +
                'Close the current session, before starting a new one.'
            )

        return BookingSession.objects.create(
            workpackage_id=workpackage.id,
            db=project,
            user=user,
        )
