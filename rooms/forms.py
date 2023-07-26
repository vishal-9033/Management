from django import forms
from rooms.models import RoomType, Room

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['room_type', 'name', 'capacity']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'type', 'room_image','price','description']

        widgets ={

            'hotel': forms.HiddenInput
        }
        
        def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['hotel'].required = False