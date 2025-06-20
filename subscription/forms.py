# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import SubscriberProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    mac_address = forms.CharField(max_length=17)
    ip_address = forms.GenericIPAddressField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'mac_address', 'ip_address']

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = SubscriberProfile
        fields = ['mac_address', 'ip_address']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.email = self.cleaned_data['email']
            self.user.first_name = self.cleaned_data.get('first_name', '')
            self.user.last_name = self.cleaned_data.get('last_name', '')
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile