from rest_framework.exceptions import APIException

class InvalidDataError(APIException):
    status_code = 400
    default_detail = 'Invalid data provided.'
    default_code = 'invalid_data'


class CustomPermissionError(APIException):
    status_code = 403
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'permission_denied'