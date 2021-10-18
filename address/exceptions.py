from rest_framework.exceptions import APIException


class NoDataException(APIException):
    status_code = 400
    default_detail = "No Data is passed"

