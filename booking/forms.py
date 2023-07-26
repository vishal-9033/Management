from django import forms
from django.forms.models import inlineformset_factory
from .models import Booking, Guest

class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['check_in_date'].required = True
        self.fields['check_out_date'].required = True

    class Meta:
        model = Booking
        fields = [ 'check_in_date','check_out_date']

        widgets = {
            'check_in_date': forms.DateInput(attrs = {'style': 'front-size: 13px; cursor: pointer', 'type':'Date','onkeydown': 'return false'}),
            'check_out_date': forms.DateInput(attrs = {'style': 'front-size: 13px; cursor: pointer', 'type':'Date','onkeydown': 'return false'}),
            'room': forms.HiddenInput,
            'User': forms.HiddenInput 
        }


class GuestForm(forms.ModelForm):
    
    class Meta:
        model = Guest
        fields = ['guest_name', 'guest_gender', 'email', 'phone_number', 'PHOTO_ID']

        widgets = {'booking': forms.HiddenInput(),}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['guest_name'].required = True
            self.fields['guest_gender'].required = True
            self.fields['email'].required = True
            self.fields['phone_number'].required = True
            self.fields['PHOTO_ID'].required = True
