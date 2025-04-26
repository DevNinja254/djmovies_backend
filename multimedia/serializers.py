from rest_framework import serializers
from .models import *
from members.models import Purchased
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = "__all__"
class AdditionalVideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalVideoFile
        fields = "__all__"
class VideoUploadSerializer(serializers.ModelSerializer):
    additional_files = AdditionalVideoFileSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    # image_url = serializers.SerializerMethodField()
    # video_url = serializers.SerializerMethodField()
    class Meta:
        model = VideoUpload
        fields = "__all__"
    # def get_image_url(self, obj):
    #     if obj.image:
    #         return self.context['request'].build_absolute_uri(obj.image.url)
    #     return None
    # def get_video_url(self, obj):
    #     if obj.video:
    #         return self.context['request'].build_absolute_uri(obj.video.url)
    #     return None
class LimitedLatestRelatedObjectsField(serializers.ListField):
    def to_representation(self, queryset):
        # Limit the number of related objects to 3
        limited_queryset = queryset.order_by("-date_uploaded")[:13]
        serializer = VideoUploadSerializer(limited_queryset,many=True, read_only=True)
        return serializer.data
class GenreSerializer(serializers.ModelSerializer):
    video_details = LimitedLatestRelatedObjectsField()
    total_related_count = serializers.SerializerMethodField()
    class Meta:
        model = Genre
        fields = "__all__"
    def get_total_related_count(self, instance):
        return instance.video_details.count()
class GenreTotalSerializer(serializers.ModelSerializer):
    total_related_count = serializers.SerializerMethodField()
    class Meta:
        model = Genre
        fields = "__all__"
    def get_total_related_count(self, instance):
        return instance.video_details.count()
class DjSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dj
        fields = '__all__'
class LimitedLatestDj(serializers.ListField):
    def to_representation(self, queryset):
        # Limit the number of related objects to 3
        limited_queryset = queryset.order_by("-date_uploaded")[:5]
        serializer = VideoUploadSerializer(limited_queryset,many=True, read_only=True)
        return serializer.data
class DjTotalSerializer(serializers.ModelSerializer):
    video_details =  LimitedLatestDj()
    class Meta:
        model = Dj
        fields = '__all__'