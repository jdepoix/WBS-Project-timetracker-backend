from rest_framework import mixins, viewsets

from core.api.permissions import IsAuthenticatedOrPostOnly

from data.wbs_user.models import WbsUser

from api.users.filters import WbsUserFilter
from api.users.serializers import WbsUserSerializer, WbsUserUpdateSerializer, WbsUserProjectSerializer


class WbsUserModelViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    ### Endpoints:

    ```[GET]		/api/users/(?(username))```

        lists all users

        PARAMS:
        - username: <String>
            filter by the users username. Note that usernames are unique.

    ```[POST]		/api/users/```

        creates a new user

        POST DATA:
        {
            /** new users username */
            username: <String>,
            /** new users password */
            password: <String>
        }

    ```[GET]		/api/users/<user_id>/```

        the user with the user id `<user_id>`.

    ```[PATCH]		/api/users/<user_id>/```

        change password of the user with the user id `<user_id>`.

        POST DATA:
        {
            /** the users old password */
            oldPassword: <String>,
            /** the users new password */
            newPassword: <String>
        }

    ```[GET]		/api/users/<user_id>/projects/```

        get all projects ot the user with the user id `<user_id>`.

    ```[POST]		/api/users/<user_id>/projects/```

        add the user to an already existing project

        POST DATA:
        {
            /** URL of the project you want the user to be added to */
            project: <URL>
        }
    """
    filter_class = WbsUserFilter
    permission_classes = (IsAuthenticatedOrPostOnly,)
    queryset = WbsUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return WbsUserUpdateSerializer
        else:
            return WbsUserSerializer


class WbsUserProjectsModelViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    ### Endpoints:

    ```[GET]		/api/users/(?(username))```

        lists all users

        PARAMS:
        - username: <String>
            filter by the users username. Note that usernames are unique.

    ```[POST]		/api/users/```

        creates a new user

        POST DATA:
        {
            /** new users username */
            username: <String>,
            /** new users password */
            password: <String>
        }

    ```[GET]		/api/users/<user_id>/```

        the user with the user id `<user_id>`.

    ```[PATCH]		/api/users/<user_id>/```

        change password of the user with the user id `<user_id>`.

        POST DATA:
        {
            /** the users old password */
            oldPassword: <String>,
            /** the users new password */
            newPassword: <String>
        }

    ```[GET]		/api/users/<user_id>/projects/```

        get all projects ot the user with the user id `<user_id>`.

    ```[POST]		/api/users/<user_id>/projects/```

        add the user to an already existing project

        POST DATA:
        {
            /** URL of the project you want the user to be added to */
            project: <URL>
        }
    """
    serializer_class = WbsUserProjectSerializer

    def get_user_from_url(self):
        """
        retrieves the WbsUser from the url

        :return: the user
        :rtype: WbsUser
        """
        return WbsUser.objects.get(pk=self.kwargs.get('user_id'))

    def get_queryset(self):
        return self.get_user_from_url().projects.all()
