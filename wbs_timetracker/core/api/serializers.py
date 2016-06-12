from rest_framework import serializers


class BaseModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

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
    def default_serializer_factory(model_object):
        """
        factory for a default serializer class

        :param model_object: the model the serializer is created for
        :return: a default serializer class
        """
        class DefaultSerializer(BaseModelSerializer):
            class Meta:
                model = model_object

        return DefaultSerializer
