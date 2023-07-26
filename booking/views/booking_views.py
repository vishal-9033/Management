import datetime
import json
from django import forms
from django.db.models.query import QuerySet
from django.forms import inlineformset_factory,formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, render,redirect
from booking.forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from booking.models import *
from rooms.models import *
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from user.models import HotelUser
from django.contrib import messages

#room_check
class CheckRoomCreateView(LoginRequiredMixin,CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'user_templates/booking.html'



    def form_valid(self, form):
        users = HotelUser.objects.get(id=self.request.user.id)
        # print(u)
        Rooms = Room.objects.get(id=self.kwargs['pk'])
        print(Rooms)
        form.instance.User = users
        form.instance.room = Rooms
        room_id = self.kwargs['pk']
        print('room id is :',room_id)
        room_obj = get_object_or_404(Room, id=room_id)

        start_date = form.cleaned_data['check_in_date']
        end_date = form.cleaned_data['check_out_date']


        print('=============== user insreted date are ===============')
        dates_between = []
        current_date = start_date
        while current_date <= end_date:
            dates_between.append(current_date)
            current_date += datetime.timedelta(days=1)
        print(dates_between)


        print('========= dates from data table ===========')
        booking_obj = Booking.objects.filter(room=room_obj)
        booked_dates = []
        for booked in booking_obj:
            current_date = booked.check_in_date
            while current_date <= booked.check_out_date:
                booked_dates.append(current_date)
                current_date += datetime.timedelta(days=1)
        print(booked_dates)

        if any(date in booked_dates for date in dates_between):
            messages.add_message(
            self.request,
            messages.INFO,
            "Room is already booked for this date. Please try another date or select another room in our hotel."
            )
            return self.form_invalid(form)
        print('*50'*50,)
        data_to_pass = {
            'check_in': start_date,
            'check_out': end_date,
            'room':room_obj
        }
        date_str = start_date.isoformat()
        date_str = end_date.isoformat()
        room_dict = room_obj.id
        self.request.session['data_to_pass'] = data_to_pass
        data_to_pass = {
            'check_in': json.dumps({'start_date': date_str}),
            'check_out': json.dumps({'end_date': date_str}),
            'room':json.dumps({'room_obj': room_dict})

        }
        print('====='*50)
        self.request.session['data_to_pass'] = data_to_pass

        # return HttpResponseRedirect(reverse_lazy('booking:GuestForm', kwargs={'pk': room_obj.id}) + '?check_in={}&check_out={}&room={}'.format(data_to_pass['check_in'], data_to_pass['check_out'], data_to_pass['room']))
        return HttpResponseRedirect(
            reverse_lazy('booking:GuestForm', kwargs={'pk': room_obj.id})
            + f"?check_in={data_to_pass['check_in']}&check_out={data_to_pass['check_out']}&room={data_to_pass['room']}"
        )
        # return reverse('booking:GuestForm', kwargs = {'pk': self.kwargs['pk']})


#createbooking form InlineView (guestfields_InlineView)
class GuestInline(InlineFormSetFactory):
    model = Guest
    # form_class = GuestForm
    fields = ['guest_name', 'guest_gender', 'email', 'phone_number', 'PHOTO_ID']
    factory_kwargs = {'extra': 1, 'max_num': None,'can_order': False, 'can_delete': False}
    # prefix = 'Guest-form'


class GuestFormCreateView(LoginRequiredMixin, CreateWithInlinesView):
    model = Booking
    inlines = [GuestInline]
    fields = ['check_in_date','check_out_date']
    template_name = 'user_templates/room_booking_form.html'

    def forms_valid(self, formset, inlines):
        check_in_json = self.request.GET.get('check_in')
        check_out_json = self.request.GET.get('check_out')

        # convert jason into python
        check_in_data = json.loads(check_in_json)
        check_out_data = json.loads(check_out_json)

        # Extract the desired values from the deserialized data
        start_date = check_in_data['start_date']
        end_date = check_out_data['end_date']
        room_obj = Room.objects.get(id=self.kwargs['pk'])
        booking = Booking.objects.create(check_in_date = start_date,check_out_date = end_date,room = room_obj,User = self.request.user)

        booking.save()
        response = self.form_valid(formset)
        for formset in inlines:
            formset.save()
        return response

    def forms_invalid(self, form, inlines):
        print(form.errors)
        form.instance.booking  = Booking.objects.latest('id')
        print(form.instance.booking)
        print(form.cleaned_data.get('data'))
        print('********invalid********')
        return self.render_to_response(self.get_context_data(form=form, inlines=inlines))
    
    def get_success_url(self):
        return reverse('booking:BookingList' ,kwargs={'pk': self.request.user.id})
    


    # def get_success_url(self):
    #     return reverse('booking:BookingList')
    #     # return self.object.get_absolute_url()
    
    
    




# GuestInlineFormSet = inlineformset_factory(Booking, Guest,form=GuestForm,extra=1, can_delete=False)
# class GuestFieldsCreateView(LoginRequiredMixin, CreateWithInlinesView):
#     model = Booking
#     fields = ['id', 'check_in','check_out']
#     # form_class = GuestInlineFormSet
#     template_name = 'user_templates/room_booking_form.html'
    
#     inlines = [GuestInlineFormSet]

#     def get_context_data(self, **kwargs):
#         #
#         context = super().get_context_data(**kwargs)
#         room_num = self.kwargs['pk']
#         context['room_num'] = room_num
#         hotel_obj = Hotel.objects.get(room=room_num)
#         context["hotel"] = hotel_obj.id
#         check_in_json = self.request.GET.get('check_in')
#         check_out_json = self.request.GET.get('check_out')

#         # Deserialize the JSON data (to convert jason data into python object)
#         check_in_data = json.loads(check_in_json)
#         check_out_data = json.loads(check_out_json)

#         # Extract the desired values from the deserialized data(to get the values of start date and end date)
#         start_date = check_in_data['start_date']
#         end_date = check_out_data['end_date']

#         # Use the extracted values in the context
#         context['check_in'] = start_date
#         context['check_out'] = end_date

#         return context

#     def forms_valid(self, form, inlines):
#         check_in_json = self.request.GET.get('check_in')
#         check_out_json = self.request.GET.get('check_out')

#         # convert jason into python
#         check_in_data = json.loads(check_in_json)
#         check_out_data = json.loads(check_out_json)

#         # Extract the desired values from the deserialized data
#         start_date = check_in_data['start_date']
#         end_date = check_out_data['end_date']
#         room_obj = Room.objects.get(id=self.kwargs['pk'])
#         print('======================')
#         print(start_date, end_date)
#         booking = form.save(commit=False)
#         print("====================",type(booking))
#         booking = form.save(commit=False)
#         booking.User = self.request.user
#         booking.room = room_obj
#         booking.check_in_date = start_date
#         booking.check_out_date = end_date
#         booking.save()


#         guest_formset_class = inlineformset_factory(Booking, Guest, form=GuestForm, extra=1, can_delete=False)
#         guest_formset = guest_formset_class(data=self.request.POST, instance=booking)
#         if guest_formset.is_valid():
#             guest_formset.save()
#             return redirect(self.get_success_url())

#     def forms_invalid(self, form, inlines):
#         print(form.errors)
#         form.instance.latest_booking  = Booking.objects.latest('id')
#         print('********invalid********')
#         print(form)
#         return self.render_to_response(self.get_context_data(form=form))
#         # return self.render_to_response(self.get_context_data(form=form, inlines=inlines))
    
    
#     def get_success_url(self,*args,**kwargs):
#         return reverse('booking:BookingList' ,kwargs={'pk': self.request.user.id})
#         # return reverse('booking:BookingList' ,kwargs={'pk': self.object.pk})


#the list of the room that the user is booking in booking list user side (front end side)
class BookingListView(LoginRequiredMixin,ListView):
    model = Guest
    template_name = 'user_templates/booking_profile/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(User=user)                
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = HotelUser.objects.get(id=self.kwargs['pk'])
        context['booking_list'] = Booking.objects.all()
        context["user"] = user
        return context


#list of all room booking in admin side('if' user  = super user thay seen all booking 
#    'else' user = hotel admin thay seen only those room bookings)
class ListOfBookingViewListView(LoginRequiredMixin,ListView):
    model = Booking
    template_name = 'admin_template/booking/bookedroomlist.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Booking.objects.all()
        queryset=Booking.objects.filter(User_id=self.kwargs['pk'])
        print(queryset)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = HotelUser.objects.get(id=self.kwargs['pk'])
        context['booking_list'] = Booking.objects.all()
        context["user"] = user
        context["Hotel"]= Hotel.objects.get(Hotel_admin= user)
        # context["Hotel"] = Hotel.objects.get(Hotel_admin=user)
        return context


#details of booked rooms in admin side(check_in _date,check_out_dates etc)
class DetailsOfBookingViewDetailView(DetailView):
    model = Guest
    template_name = 'admin_template/booking/bookedroomdetails.html'
    context_object_name = 'bookings'

    def get_context_data(self):
        return Guest.objects.get(guest_name=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            book = Guest.objects.get(Guest=self.kwargs['pk'])
            context['bookingdetail'] = book
        else:
            booked = Guest.objects.get(id=self.kwargs['pk'])
            datebooked = Booking.objects.filter(booking=booked)
            context['booking'] = datebooked
        return context



#for cancel booking user can cancel booking rooms user side  (front end side)
class BookingCancelDeleteView(DeleteView):
    model = Guest
    template_name = 'user_templates/booking_profile/booking_cancel.html'
    success_url = reverse_lazy('booking:booking_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.get(booking_id=self.request.user.pk)
        return queryset

    # def get_context_data(self, **kwargs):
    #     context =  super().get_context_data(**kwargs)
    #     booking_room = Booking.objects.get(id=self.kwargs['pk'])
    #     cancelbooking = Room.objects.get(Room=booking_room)
    #     context["cancel"] = cancelbooking
    #     return context
    
    # def get_success_url(self):
    #     bookingcancel = Booking.objects.get(id = self.kwargs['pk'] )
    #     return reverse_lazy('booking:BookingList', kwargs={'pk': bookingcancel.pk})

















































































































































































# #for details of the booking that wich room is booked user side (front end side)
# class BookingDetailsView(DetailView):
#     model = Guest
#     template_name = 'user_templates/booking_profile/booking_details.html'
#     context_object_name = 'bookings'

#     def get_context_data(self):
#         queryset = Guest.objects.get(guest_name=self.kwargs['pk'])
#         return queryset
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.user.is_superuser:
#             book = Guest.objects.get(Guest=self.kwargs['pk'])
#             context['bookingdetail'] = book
#         else:
#             booked = Guest.objects.get(id=self.kwargs['pk'])
#             datebooked = Booking.objects.get(booking=booked)
#             context['booking'] = datebooked
#         return context



    






# #cancel bookings by super_admin and hotel_admin
# class CancelBookingDeleteView(DeleteView):
#     model = Guest
#     template_name = 'admin_template/booking/bookedroomdelete.html'

#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         booking_room = Booking.objects.get(id=self.kwargs['pk'])
#         cancelbooking = Room.objects.get(Guest=booking_room)
#         context["cancel"] = booking_room
#         return context
    
#     def get_success_url(self):
#         bookingcancel = Booking.objects.get(Booking = self.kwargs['pk'] )
#         return reverse_lazy('booking:CancelBooking', kwargs={'pk': bookingcancel.pk})
