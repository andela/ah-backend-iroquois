from rest_framework.exceptions import APIException


class UserProfileDoesNotExist(APIException):
    status_code = 400
    default_detail = "The requested profile does not exist"
