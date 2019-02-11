from rest_framework.exceptions import APIException
from rest_framework import status


class DeleteOrChangeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Deletion or changing not allowed due to integrity'
    default_code = 'delete_change_error'