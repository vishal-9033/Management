from django.db import models
from django.core.validators import MinValueValidator
from hotels.models import Hotel
from base.models import *

# Create your models here.


class RoomType(MyModel):
    room_types = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('deluxe', 'Deluxe'),
        ('suite', 'Suite'),
    ]
    room_type = models.CharField(max_length=20, choices=room_types)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.room_type

class Room(MyModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_image = models.ImageField(upload_to='media/rooms')
    price = models.DecimalField(max_digits=8, decimal_places=2,default=None)
    description = models.TextField(default=None)


    def __str__(self):
        return f"Room {self.number} ({self.type.room_type})"


    def get_update_url(self):
        return f'/rooms/{self.pk}/update/'

    def get_delete_url(self):
        return f'/rooms/{self.pk}/delete/'
    
    def get_details_url(self):
        return f'/rooms/{self.pk}/details/'