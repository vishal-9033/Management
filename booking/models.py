from django.db import models
from base.models import *
from rooms.models import *
from user.models import *
from django.contrib import admin

# Create your models here.

class Booking(MyModel):
    User = models.ForeignKey(HotelUser, on_delete=models.CASCADE,null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE,null=True)
    check_in_date = models.DateField(null=True,blank=True)
    check_out_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return f"Booking for {self.room} and check in date{self.check_in_date} and check out date {self.check_out_date}"
    
class Guest(MyModel):

    guest_name = models.CharField(max_length=255)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE,null=True)
    guest_gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20,default=None)
    PHOTO_ID = models.ImageField(upload_to='media/photo_id',default='photo_id')

    def __str__(self):
        return self.guest_name
    

class GuestInline(admin.TabularInline):
    model = Guest
    extra = 1