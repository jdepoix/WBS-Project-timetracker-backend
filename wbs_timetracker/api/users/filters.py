import django_filters

from rest_framework import filters

from data.wbs_user.models import WbsUser


class WbsUserFilter(filters.FilterSet):
    username = django_filters.CharFilter(name='user__username')

    class Meta:
        model = WbsUser
        fields = ('username',)
