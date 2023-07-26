import random
import string
import datetime   
from celery import shared_task
from django import forms
from django.shortcuts import redirect
from booking.models import Booking
from user import hotel_admin_form
from user.models import *
from Hotel_Management.celery import app
from services.email import ReminderEmailSender 
from django.conf import settings
from datetime import date



@app.task(name="send_notification")
def send_notification():
    try:
        current_date = date.today()
        bookings = Booking.objects.filter(check_in_date=current_date)
        for booking in bookings:
            user = booking.User
            username = user.username.upper()
            subject = "This Is Reminder For Your ROOM Booking Today"
            message = (
                "Booking Details:\n\n"
                f"User: {booking.User}\n"
                f"room: {booking.room}\n"
                f"check_in_date: {booking.check_in_date}\n"
                f"check_out_date: {booking.check_out_date}\n"
            )

            email = booking.User.email
            from_email = "admin@example.com"
            to_email = [email]
            variable_dict = {"username": username, "message": message}
            ReminderEmailSender().send_email_custom(subject, from_email, to_email, variable_dict)

    except Exception as e:
        print(e)
