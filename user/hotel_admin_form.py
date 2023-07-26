from django import forms
from .models import HotelUser

class HotelAdminForm(forms.ModelForm):
    class Meta:
        model = HotelUser
        fields = ['username','email','password','user_type']

    widgets = {
        'password': forms.HiddenInput(),
        'user_type': forms.HiddenInput(),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['user_type'].required = False

