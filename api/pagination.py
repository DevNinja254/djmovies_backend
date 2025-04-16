from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    """
    Custom pagination class that allows retrieving all items if requested.
    """
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'
    max_page_size = 100
    all_items_query_param = 'all'  # Query parameter to request all items

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset based on the request.
        """
        if request.query_params.get(self.all_items_query_param):
            return list(queryset)  # Return all items without pagination

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        """
        Return a paginated response, or all items if requested.
        """
        if self.request.query_params.get(self.all_items_query_param):
            return Response(data) #return all items

        return super().get_paginated_response(data)

