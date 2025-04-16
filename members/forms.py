from .models import Member
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Member
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = "__all__"