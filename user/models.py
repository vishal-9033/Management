from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import MyModel


class HotelUser(AbstractUser,MyModel):
    USER_TYPE_CHOICES = (
        (1, "webapp_admin"),
        (2, "hotel_admin"),
        (3, "user"),
    )
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=3)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    city = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, default='M')

    REQUIRED_FIELDS = ['email']

    def get_update_url(self):
        return f'/hoteladmin/{self.pk}/update/'

    def get_detail_url(self):
        return f'/hoteladmin/{self.pk}/detail/'
    
    def get_delete_url(self):
        return f'/hoteladmin/{self.pk}/delete/'
    


    def get_detailuser_url(self):
        return f'/user/{self.pk}/details/'
    
    def get_deleteuser_url(self):
        return f'/user/{self.pk}/delete/'
    
