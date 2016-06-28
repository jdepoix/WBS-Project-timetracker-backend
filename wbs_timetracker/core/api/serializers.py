from rest_framework import serializers


class BaseModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    url_field_name = 'self'

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(BaseModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    @staticmethod
    def default_serializer_factory(model_object, model_fields=None):
        """
        factory for a default serializer class

        :param model_object: the model the serializer is created for
        :type model_object: models.Model
        :param model_fields: optional iterable of fields
        :type model_fields: iterable
        :return: a default serializer class
        """
        class DefaultSerializer(BaseModelSerializer):
            class Meta:
                model = model_object

        class DefaultCustomFieldSerializer(BaseModelSerializer):
            class Meta:
                model = model_object
                fields = model_fields

        return DefaultCustomFieldSerializer if model_fields else DefaultSerializer


class ZeroTimeDateTimeField(serializers.DateTimeField):
    """
    this is a DateTimeField which just zeros out the time component. This is needed when a datetime field is used, where
    a date field should have been used...
    """
    def to_internal_value(self, value):
        value += ' 00:00:00'
        return super(ZeroTimeDateTimeField, self).to_internal_value(value)
