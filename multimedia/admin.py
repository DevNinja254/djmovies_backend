from django.contrib import admin
from .models import  VideoUpload,AdditionalVideoFile, Genre, Dj, Category
# Register your models here.
class AdditionalVideoFileInline(admin.TabularInline):  # Or use StackedInline
    model = AdditionalVideoFile
    extra = 1  # Number of empty forms to display for adding new files

class VideoUploadEdit(admin.ModelAdmin):
    inlines = [AdditionalVideoFileInline]
    list_display=("title", "price", "genre", "dj")
    search_fields=("title",)
    readonly_fields = ("purchase_times", "likes", "date_uploaded")
    list_filter = ("genre", "price", "dj", "purchase_times")
    ordering = ("-date_uploaded",)


class GenreEdit(admin.ModelAdmin):
    list_display=("title",)
    search_fields=("title",)


class ReviewEdit(admin.ModelAdmin):
    list_display=("user", "video_title", "rate", "comment")
    list_display_links=("video_title",)
    list_editable=("rate", "comment", "user")
    search_fields=("video_title", "user")
    list_filter = ("rate",)

admin.site.register(VideoUpload, VideoUploadEdit)
admin.site.register(Genre, GenreEdit)
admin.site.register(Dj)
admin.site.register(Category)