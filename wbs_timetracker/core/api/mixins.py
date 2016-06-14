from rest_framework import mixins


class ViewSetEVACalculationManager(object):
    """
    manages starting the eva recalculation from a viewset request
    """
    @staticmethod
    def recalc_eva_values(request, *args, **kwargs):
        """
        starts the eva recalculation from a viewset request

        :param request:
        :param args:
        :param kwargs:
        """
        # TODO EVA recalc
        pass

class EVACreateModelMixin(mixins.CreateModelMixin):
    """
    this works like a CreateModelMixin, but triggers the EVA recalculation before returning the response
    """
    def create(self, request, *args, **kwargs):
        response = super(EVACreateModelMixin, self).create(request, *args, **kwargs)

        ViewSetEVACalculationManager.recalc_eva_values(request, *args, **kwargs)

        return response

class EVAUpdateModelMixin(mixins.UpdateModelMixin):
    """
    this works like a UpdateModelMixin, but triggers the EVA recalculation before returning the response
    """
    def update(self, request, *args, **kwargs):
        response = super(EVAUpdateModelMixin, self).update(request, *args, **kwargs)

        ViewSetEVACalculationManager.recalc_eva_values(request, *args, **kwargs)

        return response

class EVADestroyModelMixin(mixins.DestroyModelMixin):
    """
    this works like a DestroyModelMixin, but triggers the EVA recalculation before returning the response
    """
    def destroy(self, request, *args, **kwargs):
        response = super(EVADestroyModelMixin, self).destroy(request, *args, **kwargs)

        ViewSetEVACalculationManager.recalc_eva_values(request, *args, **kwargs)

        return response
