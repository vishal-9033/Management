from django.db import models
from base.models import * 
from user.models import HotelUser  

class Hotel(MyModel):
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    Hotel_admin = models.ForeignKey('user.HotelUser',related_name='hotel_hoteladmin',on_delete=models.CASCADE,)
    amenities = models.TextField(max_length=140, default='NONE')
    hotel_image = models.ImageField(upload_to='media/hotel')

    def __str__(self):
         return self.name

    def get_update_url(self):
        return f'/hotels/{self.pk}/update/'

    def get_delete_url(self):
        return f'/hotels/{self.pk}/delete/'
    
    def get_detail_url(self):
        return f'/hotels/{self.pk}/details/'