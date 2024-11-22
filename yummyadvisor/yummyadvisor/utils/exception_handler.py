from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "errors": response.data,
            "status_code": response.status_code
        }
    else:
        # Eğer standart DRF exception handler dışında bir hata varsa
        response = Response({
            "errors": {"detail": str(exc)},
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
