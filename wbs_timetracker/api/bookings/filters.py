import django_filters

from rest_framework import filters

from data.legacy.project.models import WorkEffort


class WorkEffortFilter(filters.FilterSet):
    workpackage_id = django_filters.NumberFilter(name='workpackage__id')
    date = django_filters.DateFilter(name='rec_date')

    class Meta:
        model = WorkEffort
        fields = ['workpackage_id', 'date',]
