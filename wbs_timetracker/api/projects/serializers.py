from abc import ABCMeta, abstractproperty

from rest_framework import serializers
from rest_framework.reverse import reverse


class SubProjectHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    """
    ABC for hyperlink related fields depending on a project
    """
    __metaclass__ = ABCMeta

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'project_id': request.parser_context.get('kwargs').get('project_id'),
            'pk': obj.pk
        }

        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        return self.model.objects.using(
            view_kwargs.get('project_id')
        ).get(
            view_kwargs.get('pk')
        )

    @abstractproperty
    def model(self):
        """
        :return: the on the project id depending model
        """
        pass
