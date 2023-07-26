from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Guest)
# admin.site.register(Booking)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    inlines = [
        GuestInline
    ]