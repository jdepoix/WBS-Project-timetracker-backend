from abc import ABCMeta, abstractmethod

from rest_framework import mixins


class ViewSetEVACalculationManager(object):
    """
    manages starting the eva recalculation from a viewset request
    """
    # TODO probably replace this as soon as EVA module is done
    @staticmethod
    def recalc_eva_values(workpackage):
        """
        :param workpackage:
        :return:
        """
        # TODO EVA recalc
        pass


class EVARecalcMixin(object):
    """
    every class implementing this mixin need to supply a method, which allows retrieving the regarding workpackage
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_workpackage(self, request, *args, **kwargs):
        """
        returns the workpackage this request is about

        :param request:
        :param args:
        :param kwargs:
        :return: the workpackage
        :rtype: Workpackage
        """
        pass

    def recalc_eva_values(self, request, *args, **kwargs):
        """
        triggers the recalculation of the eva values

        :param request:
        :param args:
        :param kwargs:
        """
        ViewSetEVACalculationManager.recalc_eva_values(self.get_workpackage(request, *args, **kwargs))


class EVACreateModelMixin(mixins.CreateModelMixin, EVARecalcMixin):
    """
    this works like a CreateModelMixin, but triggers the EVA recalculation before returning the response
    """
    __metaclass__ = ABCMeta

    def create(self, request, *args, **kwargs):
        response = super(EVACreateModelMixin, self).create(request, *args, **kwargs)

        self.recalc_eva_values(self, request, *args, **kwargs)

        return response


class EVAUpdateModelMixin(mixins.UpdateModelMixin, EVARecalcMixin):
    """
    this works like a UpdateModelMixin, but triggers the EVA recalculation before returning the response
    """
    __metaclass__ = ABCMeta

    def update(self, request, *args, **kwargs):
        response = super(EVAUpdateModelMixin, self).update(request, *args, **kwargs)

        self.recalc_eva_values(self, request, *args, **kwargs)

        return response


class EVADestroyModelMixin(mixins.DestroyModelMixin, EVARecalcMixin):
    """
    this works like a DestroyModelMixin, but triggers the EVA recalculation before returning the response
    """
    __metaclass__ = ABCMeta

    def destroy(self, request, *args, **kwargs):
        response = super(EVADestroyModelMixin, self).destroy(request, *args, **kwargs)

        self.recalc_eva_values(self, request, *args, **kwargs)

        return response
