from rest_framework.exceptions import APIException


class ArticleNotFound(APIException):
    status_code = 404
    default_detail = "The requested article does not exists"
