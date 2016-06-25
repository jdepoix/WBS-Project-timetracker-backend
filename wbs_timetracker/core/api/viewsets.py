from abc import ABCMeta

from rest_framework import viewsets, mixins

from core.api.mixins import EVACreateModelMixin, EVAUpdateModelMixin, EVADestroyModelMixin


class EVAModelViewSet(
    EVACreateModelMixin,
    EVAUpdateModelMixin,
    EVADestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    this viewset works like a ModelViewSet, but uses the EVA specific mixins for create, update and delete
    """
    __metaclass__ = ABCMeta

    pass
