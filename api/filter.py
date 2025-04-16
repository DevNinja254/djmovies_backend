import django_filters 
from multimedia.models import  VideoUpload
from members.models import Purchased, DepositHistory
from django_filters.rest_framework import FilterSet

class VideoUploadFilter(FilterSet):
    """
    Custom filter for VideoUpload model.
    """
    type = django_filters.ChoiceFilter(choices=VideoUpload.TYPE_CHOICES)
    title = django_filters.CharFilter(lookup_expr='icontains')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    date_uploaded_min = django_filters.DateTimeFilter(field_name='date_uploaded', lookup_expr='gte')
    date_uploaded_max = django_filters.DateTimeFilter(field_name='date_uploaded', lookup_expr='lte')
    popular = django_filters.BooleanFilter()
    genre = django_filters.CharFilter(field_name='genre', lookup_expr='exact') #filter by category name
    cartegory = django_filters.ChoiceFilter(field_name='cartegory', choices=VideoUpload.CART_CHOICES)

    class Meta:
        model = VideoUpload
        fields = ['type', 'title', 'price', 'date_uploaded', 'popular', "genre", "cartegory"]  # Add any other fields you want to filter by



class PurchaseFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='exact')
    
    class Meta:
        model = Purchased
        fields = ['username']  
class DepositFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='name', lookup_expr='exact')
    
    class Meta:
        model = DepositHistory
        fields = ['name']  
