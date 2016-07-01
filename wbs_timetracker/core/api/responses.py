from rest_framework.response import Response


class ErrorResponse(Response):
    """
    a response with a default status code of 400
    """
    def __init__(self, data=None, status=400,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        super(ErrorResponse, self).__init__(
            data=data,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )


class ExceptionResponse(ErrorResponse):
    """
    a response showing the details of an exception
    """
    def __init__(self, exception):
        super(ExceptionResponse, self).__init__(
            data={
                'exception': exception.__class__.__name__,
                'message': exception.message,
            }
        )
