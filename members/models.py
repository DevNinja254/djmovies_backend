from django.db import models
import random, uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
# Create your models here.
def generate_unique_id():
    return uuid.uuid4()
class Member(AbstractUser):
    id = models.UUIDField(primary_key=True, default=generate_unique_id, editable=False)
    username = models.CharField(max_length=100, unique=True, default=random.randint(1, 10000000))
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    class Meta:
        db_table = "members"

class Profile(models.Model):
    buyerid = models.UUIDField(primary_key=True, default=generate_unique_id, editable=False)
    username = models.CharField(max_length=200, default=generate_unique_id, editable=True)
    user = models.OneToOneField(Member, on_delete=models.CASCADE, related_name="profile", default="false")
    account = models.IntegerField(verbose_name="account(Ksh)", default=0,)    
    phone_number = models.IntegerField(default="0700000000")
    country = models.CharField(max_length=100, default="Kenya")
    city = models.CharField(max_length=100, default="mombasa")
    profile_pic = models.ImageField(upload_to="profile_pics/", default="profile_pics/download.png")
    def save(self, *args, **kwargs):
        self.username = str(self.user.username)
        super(Profile, self).save(*args, **kwargs)
    def __str__(self):
        return self.user.username 
    class Meta:
        db_table = "profile"
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_profile, sender=Member)
post_save.connect(save_profile, sender=Member)

class Purchased(models.Model):
    purchase_id = models.UUIDField(primary_key=True, default=generate_unique_id, editable=False)
    video_id = models.UUIDField()
    username = models.ForeignKey(Member, to_field="username", on_delete=models.CASCADE, related_name="purchase")
    video_name = models.CharField(max_length=150)
    image_url = models.URLField(default="https://images.unsplash.com/photo-1604545200457-63641121af3b?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGRhcmVkZXZpbHxlbnwwfHwwfHx8MA%3D%3D")
    price = models.IntegerField()
    purchase_time = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.username.username
    class Meta:
        db_table = "purchased"
class DepositHistory(models.Model):
    deposit_id = models.UUIDField(primary_key=True, default=generate_unique_id, editable=False)
    name = models.ForeignKey(Member, to_field="username", on_delete=models.CASCADE, related_name="deposit_history")
    amount = models.IntegerField()
    time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "deposit" 
class Paying(models.Model):
    id = models.UUIDField(primary_key=True, default=generate_unique_id, editable=False)
    username = models.UUIDField()
    phone_number = models.CharField(max_length=150)
    def __str__(self):
        return self.username
    class Meta:
        db_table = "payments"
class Notification(models.Model):
    noty_id = models.UUIDField(primary_key=True, default=generate_unique_id, editable=False)
    message = models.TextField()
    date_notified = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.message
class Paymentcode(models.Model):
    pay_id = models.UUIDField(primary_key=True, default=generate_unique_id, editable=False)
    code = models.CharField(max_length=150)
    amount = models.IntegerField()

    def __str__(self):
        return self.code
class Error(models.Model):
    error_id = models.UUIDField(default=generate_unique_id, primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="errors")
    error_details = models.TextField()
    def __str_(self):
        return self.error_details
    class Meta:
        db_table = "errors"
class Message(models.Model):
    message_id = models.UUIDField(default=generate_unique_id, primary_key=True)
    email = models.EmailField(max_length=100, blank=False)
    message = models.TextField()
    def __str__(self):
        return self.email 
    class Meta:
        db_table = "messages"