from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Member,Profile, Paymentcode, Error, DepositHistory, Message, Notification, Purchased
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Member
    list_display = ("email","username", "is_staff", "is_superuser" ,)
    list_filter = ("is_staff", "is_active",)
    search_fields = ("email", "username")
    readonly_fields = ("date_joined",)
    fieldsets = (
        (None, {"fields": ("email",)}),
        ("Permissions", {"fields": ("is_staff", "date_joined", "groups", "user_permissions")}),
    )
    list_display_links = ('email',)
    list_editable = ["username", "is_staff", "is_superuser"]
    ordering = ("-date_joined",)
    class Meta:
        db_table = "Members"


class DepositHistoryEdit(admin.ModelAdmin):
    list_display=("name","amount", "time",)
    search_fields=("name", "amount")
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ("time",)
    fieldsets = ()
    ordering = ("-time", )

class MessageEdit(admin.ModelAdmin):
    list_display=("email", "message")
    search_fields=("email",)
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()
class PurchasedAdmin(admin.ModelAdmin):
    list_display=("username", "video_name", "price", "purchase_time")
    list_display_links = ("username", "video_name")
    search_fields=("username",)
    ordering = ("-purchase_time", )
class Paymentcod(admin.ModelAdmin):
    list_display = ("code", "amount",)
    search_fields = ["code"]
class Buyer(admin.ModelAdmin):
    list_display = ("user",'account', "username")
    search_fields = ["username"]
class ErrosSetting(admin.ModelAdmin):
    list_display = ("error_id", "error_details")
    search_fields = ["error_id"]

admin.site.register(Member, CustomUserAdmin)
admin.site.register(Profile, Buyer )
admin.site.register(DepositHistory, DepositHistoryEdit)
admin.site.register(Message, MessageEdit)
admin.site.register(Notification)
admin.site.register(Paymentcode, Paymentcod)
admin.site.register(Purchased, PurchasedAdmin)
admin.site.register(Error, ErrosSetting)
