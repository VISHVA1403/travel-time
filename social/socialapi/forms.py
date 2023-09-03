from django.forms import ModelForm
from .models import UserProfile


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_photo','bio','favorite_destinations','travel_style','wishlist']