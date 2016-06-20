from rest_framework.views import APIView
from rest_framework.response import Response

from core.api.responses import ErrorResponse

from data.wbs_user.models import WbsUser


#TODO rework the way booking sessions work
class BookingSessionsViewSet(APIView):
    """
    ```[GET]		booking-session/```

        list the current booking session for the currently logged in user, in case there is an open session.

    ```[POST]		booking-session/```

        open a new booking session for the currently logged in user.

        POST DATA:
        {
            /** timestamp of the beginning of the booking session */
            timestamp: <timestamp>
        }

    ```[DELETE]     booking-session/```

        close the current booking session and make the booking
    """
    queryset = WbsUser.objects.all()

    def get(self, request):
        return Response({
            'timestamp': request.user.wbs_user.start_current_booking_session
        })

    def create(self, request):
        if request.user.wbs_user.start_current_booking_session:
            return ErrorResponse({
                'error': 'There already is a ongoing booking session. Close the current session, before starting a new one'
            })
