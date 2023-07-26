from django import forms
from hotels.models import Hotel
from user.models import HotelUser

class AddHotelForm(forms.ModelForm):

    class Meta:

        model = Hotel
        fields = ['name','description','location','amenities','hotel_image','Hotel_admin']


    def init(self, args, **kwargs):
        #hotel admin ma je hotel admin hoy eva j user batave e quary set no use karyo 6
        super().init(args, kwargs)
        self.fields['Hotel_admin'].queryset = HotelUser.objects.filter(user_type = 2)
        for name, field in self.fields.items():
            if name in ['amenities','description']:
                field.widget.attrs.update({'class': 'form-control', 'rows': 2})
            else:
                field.widget.attrs.update({'class': 'form-control'})



class UpdateHotel(forms.ModelForm):

    class Meta:

        model = Hotel
        fields = ['name','description','location','amenities','hotel_image','Hotel_admin']


    def init(self, args, **kwargs):

        super().init(args, kwargs)
        self.fields['Hotel_admin'].queryset = HotelUser.objects.filter(user_type = 2)
        for name, field in self.fields.items():
            if name in ['amenities','description']:
                field.widget.attrs.update({'class': 'form-control', 'rows': 2})
            else:
                field.widget.attrs.update({'class': 'form-control'})