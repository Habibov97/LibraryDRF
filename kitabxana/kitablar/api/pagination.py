from rest_framework.pagination import PageNumberPagination

class SmallPagination(PageNumberPagination):
    page_size = 3

class LargePagination(PageNumberPagination):
    page_size = 15
