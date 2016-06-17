from django.forms import NullBooleanField
from django.forms.widgets import Select
from django.utils.translation import ugettext_lazy
from django_filters.filters import BooleanFilter


class WBSNullBooleanSelect(Select):
    """
    works the same as a NullBooleanSelect, but uses a workaround to allow for non capital True and False values
    """

    VALUE_LOOKUP_TABLE = {
        'null': None,
        'true': True,
        'false': False,
    }

    REVERSE_VALUE_LOOKUP_TABLE = {
        value: key for key, value in VALUE_LOOKUP_TABLE.iteritems()
    }

    def __init__(self, attrs=None):
        choices = (('null', ugettext_lazy('dont\'t filter')),
                   ('true', ugettext_lazy('true')),
                   ('false', ugettext_lazy('false')))
        super(WBSNullBooleanSelect, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        try:
            value = WBSNullBooleanSelect.REVERSE_VALUE_LOOKUP_TABLE.get(value)
        except KeyError:
            value = 'null'
        return super(WBSNullBooleanSelect, self).render(name, value, attrs, choices)

    def value_from_datadict(self, data, files, name):
        return WBSNullBooleanSelect.VALUE_LOOKUP_TABLE.get(data.get(name))


class WBSNullBooleanField(NullBooleanField):
    """
    works the same as a NullBooleanField, but uses a workaround to allow for non capital True and False values
    """
    widget = WBSNullBooleanSelect


class WBSNullBooleanFilter(BooleanFilter):
    """
    works the same as a BooleanFilter, but uses a workaround to allow for non capital True and False values
    """
    field_class = WBSNullBooleanField
