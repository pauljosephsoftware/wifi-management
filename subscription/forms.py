# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import SubscriberProfile

class UserRegistrationForm(forms.ModelForm):
    model= SubscriberProfile
    password = forms.CharField(widget=forms.PasswordInput)
    mac_address = forms.CharField(max_length=17)
    ip_address = forms.GenericIPAddressField()
    profile_pic = forms.ImageField(required=False)
    phone_number = forms.CharField(max_length=15)
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'mac_address', 'ip_address']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile = user.subscriberprofile  # assuming a post_save signal creates it
            profile.profile_pic = self.cleaned_data.get('profile_pic')
            profile.mac_address = self.cleaned_data.get('mac_address')
            profile.ip_address = self.cleaned_data.get('ip_address')
            profile.phone_number = self.cleaned_data.get('phone_number')
            profile.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    model = SubscriberProfile
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    profile_pic = forms.ImageField(required=False)
    

    class Meta:
        model = SubscriberProfile
        fields = ['mac_address', 'ip_address']

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile = user.subscriberprofile  # assuming a post_save signal creates it
            profile.profile_pic = self.cleaned_data.get('profile_pic')
            profile.save()
        return user

    