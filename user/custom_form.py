# from allauth.account.forms import SignupForm
from django import forms
from .models import HotelUser
from allauth.account.forms import SignupForm
# from .models import HotelAdmin

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    city = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = HotelUser
        fields = ['first_name', 'last_name', 'username','city', 'phone_number', 'email', 'date_of_birth', 'gender']
