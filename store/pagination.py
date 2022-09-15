from rest_framework.pagination import LimitOffsetPagination

class DefaultLimitOffsetPagination(LimitOffsetPagination):
    page_size = 10