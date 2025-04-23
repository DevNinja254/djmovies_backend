from django.db import models
from django.utils import timezone
import uuid
# Create your models here.
def generate_unique_id():
    return uuid.uuid4()
# Action Horror Adventure Comedy Sci fi ROmanace
class Genre(models.Model):
    cartId = models.UUIDField(primary_key=True, default=generate_unique_id, editable=False)
    title = models.CharField(max_length=50, null=False, unique=True)
    image = models.ImageField(upload_to="genre/", default="https://images.unsplash.com/photo-1579713899713-bcd3efe713aa?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()
        super().save(*args, **kwargs)
    class Meta:
        db_table = "cartegories"

class Dj(models.Model):
    id = models.UUIDField(primary_key=True, default=generate_unique_id, editable=False)
    dj_name = models.CharField(max_length=150, unique=True)
    def save(self, *args, **kwargs):
        self.dj_name = self.dj_name.capitalize()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.dj_name
class Category(models.Model) :
    id = models.UUIDField(primary_key=True, default=generate_unique_id, editable=False)
    category_name = models.CharField(max_length=100, null=False, unique=True)
    def __str__(self):
        return self.category_name
class VideoUpload(models.Model):
    vidId = models.UUIDField(primary_key=True, default=generate_unique_id, editable=False)
    title = models.CharField(max_length=100, null=False, unique=True)
    price = models.IntegerField()
    genre = models.ForeignKey(Genre, to_field="title", on_delete=models.CASCADE, related_name="video_details", default="Action")
    dj = models.ForeignKey(Dj, to_field="dj_name", verbose_name="video Type", on_delete=models.CASCADE)
    synopsis = models.TextField()
    date_uploaded = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="videoImage/")
    popular = models.BooleanField(default=False)
    season = models.CharField(max_length=150, default="season 1")
    purchase_times = models.IntegerField(default=0)
    video = models.FileField(upload_to="videos/")
    likes = models.IntegerField(default=0)
    cartegory = models.ForeignKey(Category,to_field="category_name", on_delete=models.CASCADE, related_name='video')
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()  # Convert name to lowercase
        super().save(*args, **kwargs)
    class Meta:
        db_table = "uploads"
class AdditionalVideoFile(models.Model):
    video_upload = models.ForeignKey(VideoUpload, related_name='additional_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='additional_videos/')
    class Meta:
        db_table = "additional_video_files"
class Review(models.Model) :
    id = models.UUIDField(primary_key=True, default=generate_unique_id, editable=False)
    user = models.CharField(max_length=150, default="anonymous")
    video_title = models.ForeignKey(VideoUpload, on_delete=models.CASCADE, related_name="reviews")
    rate = models.IntegerField()
    comment = models.TextField()
    def __str__(self):
        return self.user
