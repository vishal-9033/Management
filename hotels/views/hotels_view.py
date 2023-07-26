from django.db.models import Q
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render,redirect
from hotels.forms import AddHotelForm,UpdateHotel
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from base.mixin import *
from django.urls import reverse_lazy
from hotels.models import Hotel
from user.models import HotelUser
from django.http import JsonResponse
from django.views.generic import View
from django_datatables_too.mixins import DataTableMixin


#hotel_admin
class HotelListView(SuperUserRequiredMixin,ListView):
    model = Hotel
    template_name = 'admin_template/hotel/hotel_list.html'
    context_object_name = 'hotels'
    queryset = Hotel.objects.none()
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        hotel = Hotel.objects.all()
        context['Hotel'] = hotel
        return context

class DataTablesAjaxPagination(DataTableMixin, View):
    
    queryset = Hotel.objects.all()

    def _get_actions(self, obj):
        return f'<a href="{obj.get_update_url()}" title="Edit" class="btn btn-primary"><i class="bi bi-pen-fill"></i></a> <a data-title="{obj}" title="detail" href="{obj.get_detail_url()}" class="btn btn-info"><i class="bi bi-info-lg"></i></a> <a data-title="{obj}" title="Delete" href="{obj.get_delete_url()}" class="btn btn-danger btn-xs btn-delete"><i class="bi bi-trash-fill"></i></a>'
    def filter_queryset(self, qs):
        if self.search:
            return qs.filter(
                Q(id__icontains=self.search) |
                Q(name__icontains=self.search) |
                Q(location__icontains=self.search)
            )
        # print('==================================>qs==',qs)
        return qs

    def prepare_results(self, qs):
        data = []
        for o in qs:
            data.append({
                'id': o.id,
                'name': o.name,
                'location': o.location,
                'actions': self._get_actions(o)
            })
        # print('==================================>data==',data)
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)


    
class AddHotelView(SuperUserRequiredMixin,CreateView):
    form_class = AddHotelForm
    template_name = 'admin_template/hotel/hotel_add.html'

    def form_valid(self, form):
        form.save()
        return redirect('hotels:all')
    
    

class UpdateHotelView(SuperUserRequiredMixin,UpdateView):
    model = Hotel
    form_class = UpdateHotel
    template_name = 'admin_template/hotel/hotel_update.html'
    success_url = reverse_lazy ('hotels:all')



class DeleteHotelView(SuperUserRequiredMixin,DeleteView):
    model = Hotel
    template_name = 'admin_template/hotel/hotel_delete.html'
    success_url = reverse_lazy('hotels:all')



class HotelDetailView(AllAdminMixin,DetailView):
    model = Hotel
    template_name = 'admin_template/hotel/hotel_details.html'
    context_object_name = 'hotels'


    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            hotel = Hotel.objects.all()
        else:
            hotel =  Hotel.objects.get(Hotel_admin=self.request.user)
        context['Hotel'] = hotel
        return context


class HotelViewListView(LoginRequiredMixin,ListView):
    model = Hotel
    template_name = 'user_templates/hotel.html'
    context_object_name = 'hotels'

#admin_dashbord
class Super_AdminView(AllAdminMixin,TemplateView):
    template_name = 'admin_template/deshboard.html' 

    #to check that super admin can acces all and hotel admin can not access alll fields
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            hotel = Hotel.objects.all()
        else:
            User = HotelUser.objects.get(id=self.request.user.id)
            print(User.first_name)
            hotel =  Hotel.objects.get(Hotel_admin=self.request.user)
        context['Hotel'] = hotel
        return context