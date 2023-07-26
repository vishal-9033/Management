from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from allauth.account.forms import SignupForm
from requests import request
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, RedirectView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from booking.models import Booking
from services.email import EmailSender
from user.hotel_admin_form import HotelAdminForm
from user.models import *
from hotels.models import *
from rooms.models import *
from booking.models import *
from base.mixin import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
import random
import string
from django.http import HttpResponse
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import View
from django_datatables_too.mixins import DataTableMixin


# hotelAdminList Admin Side
class HotelAdminListView(SuperUserRequiredMixin, ListView):

    model = HotelUser
    template_name = 'admin_template/hotel_admin/hotel_admin_list.html'
    context_object_name = 'hotel_admins'
    queryset = HotelUser.objects.none()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Hotel'] = Hotel.objects.all()
        return context


class DataTablesAjaxPagination_HotelAdmin(DataTableMixin, View):

    # filter user_type in user is hotel_admin
    def get_queryset(self):
        return HotelUser.objects.filter(user_type =2)


    def _get_actions(self, obj):
        """Get action buttons w/links."""
        return f'<a href="{obj.get_update_url()}" title="Edit" class="btn btn-primary"><i class="bi bi-pen-fill"></i></a> <a data-title="{obj}" title="detail" href="{obj.get_detail_url()}" class="btn btn-info"><i class="bi bi-info-lg"></i></a> <a data-title="{obj}" title="Delete" href="{obj.get_delete_url()}" class="btn btn-danger btn-xs btn-delete"><i class="bi bi-trash-fill"></i></a>'

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:

            return qs.filter(

                Q(id__icontains=self.search) |
                Q(username__icontains=self.search) |
                Q(email__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append({
                'id': o.id,
                'username': o.username,
                'email': o.email,
                'actions': self._get_actions(o)
            })
        return data

    def get(self, request):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)

# To create Hotel_admin
class HotelAdminCreateView(SuperUserRequiredMixin, CreateView):
    model = HotelUser
    form_class = HotelAdminForm
    template_name = 'admin_template/hotel_admin/hotel_admin_create.html'
    success_url = reverse_lazy('hotel_admins:hoteladmin_list')


# auto generate password for Hotel_Admin

    def form_valid(self, form):
        hotel_admin = form.save()
        username = form.cleaned_data["username"]
        password = ''.join(
            [random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])
        hotel_admin.set_password(password)
        form.instance.user_type = 2
        hotel_admin.save()
        subject = 'Mail is sending to the HotelAdmin'
        from_email = 'HotelierAdmin@hotel.com'
        to_email = [hotel_admin.email]
        variable_dict = {"username": username, "password": password}
        EmailSender.send_email_custom(
            subject, from_email, to_email, variable_dict=variable_dict)
        return redirect('hotel_admins:hoteladmin_list')


class HotelAdminDetailView(SuperUserRequiredMixin, DetailView):
    model = HotelUser
    template_name = 'admin_template/hotel_admin/hotel_admin_detail.html'
    context_object_name = 'hotel_admins'


class HotelAdminUpdateView(SuperUserRequiredMixin, UpdateView):
    model = HotelUser
    form_class = HotelAdminForm
    template_name = 'admin_template/hotel_admin/hotel_admin_update.html'
    success_url = reverse_lazy('hotel_admins:hoteladmin_list')

    


class HotelAdminDeleteView(SuperUserRequiredMixin, DeleteView):
    model = HotelUser
    template_name = 'admin_template/hotel_admin/hotel_admin_delete.html'
    success_url = reverse_lazy('hotel_admins:hoteladmin_list')
