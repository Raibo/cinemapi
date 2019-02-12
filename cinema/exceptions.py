from rest_framework.exceptions import APIException
from rest_framework import status


class DeleteOrChangeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Deletion or changing not allowed due to integrity'
    default_code = 'delete_change_error'


class SessionTimeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Session can not start before cinema opens or close after it closes'
    default_code = 'session_time_error'


class SessionIntersectError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Sessions should not intersect with each other'
    default_code = 'session_intersect_error'


class WrongSeatError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Seat unavailable or does not exist'
    default_code = 'wrong_seat_error'


class BookTooLateError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Too late to book'
    default_code = 'book_too_late_error'


class PayOnlyPatchError(APIException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = 'Use \"PATCH\" method'
    default_code = 'buy_only_patch_error'


class AlreadyPaidError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Already paid'
    default_code = 'already_paid_error'
