from rest_framework import filters

from core.api.filters import WBSNullBooleanFilter

from data.legacy.project.models import Workpackage


class WorkpackageFilter(filters.FilterSet):
    toplevel_wp = WBSNullBooleanFilter(name='is_toplevel_wp')
    inactive = WBSNullBooleanFilter(name='is_inactive')

    class Meta:
        model = Workpackage
        fields = ['toplevel_wp', 'inactive',]
