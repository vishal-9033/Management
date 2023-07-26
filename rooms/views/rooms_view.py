from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404, render,redirect
from rooms.forms import RoomForm,RoomTypeForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from rooms.models import  *
from hotels.models import *
from base.mixin import *
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import View
from django_datatables_too.mixins import DataTableMixin


class RoomListView(AllAdminMixin,ListView):
    model = Room
    template_name = 'admin_template/rooms/room_list.html'
    context_object_name = 'rooms'
    queryset = Room.objects.none()

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        hotl = Hotel.objects.get(id=self.kwargs['pk'])
        context['Hotel'] = hotl
        return context

class DataTablesAjaxPaginationRooms(DataTableMixin, View):
    
    def get_queryset(self):
        print('===============================')
        print(self.kwargs['pk'] )
        
        return Room.objects.filter(hotel=self.kwargs['pk'])

    def _get_actions(self, obj):
        return f'<a href= "{obj.get_update_url()}" title="Edit" class="btn btn-primary"><i class="bi bi-pen-fill"></i></a> <a data-title="{obj}" title="detail" href="{obj.get_details_url()}" class="btn btn-info"><i class="bi bi-info-lg"></i></a> <a data-title="{obj}" title="Delete" href="{obj.get_delete_url()}" class="btn btn-danger btn-xs btn-delete"><i class="bi bi-trash-fill"></i></a>'

    def filter_queryset(self, qs):
        if self.search:
            return qs.filter(

                # Q(id__icontains=self.search)|
                Q(number__icontains=self.search) |
                Q(price__icontains=self.search) 
            )
        return qs
    
    def prepare_results(self, qs):
        data = []
        for o in qs:
            data.append({
                # 'id':o.id,
                'number': o.number,
                'price': o.price,
                'actions': self._get_actions(o)
            })
        return data

    def get(self, request):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)
      

class RooomDetailView(AllAdminMixin,DetailView):
    model = Room
    template_name = 'admin_template/rooms/room_details.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        queryset = Room.objects.filter(id=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            hotl = Hotel.objects.get(room=self.kwargs['pk'])
            context['Hotel'] = hotl
        else:
            room = Room.objects.get(id=self.kwargs['pk'])
            hotl = Hotel.objects.get(room=room)
            context['Hotel'] = hotl
        return context
    

class AddRoomView(AllAdminMixin,CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'admin_template/rooms/room_add.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        hotl = Hotel.objects.get(id=self.kwargs['pk'])
        context['Hotel'] = hotl
        return context


    def form_valid(self, form):
        hotel_name = self.kwargs['pk']
        hotel_obj = get_object_or_404(Hotel,id=hotel_name)
        form.instance.hotel = hotel_obj
        return super().form_valid(form)
    
    
    def get_success_url(self):
        return reverse_lazy('rooms:admin_rooms', kwargs={'pk':self.kwargs['pk']})
    

class UpdateRoomView(AllAdminMixin,UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'admin_template/rooms/room_update.html'



    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        user = HotelUser.objects.get(id=self.request.user.id)
        print(user)
        room_obj= Room.objects.get(id=self.kwargs['pk'])
        hotlupdate = Hotel.objects.get(room = room_obj)
        context['Hotel'] = hotlupdate
        return context
    

    def get_success_url(self):
        Hoteldelete = Hotel.objects.get(room = self.kwargs['pk'])
        return reverse_lazy('rooms:admin_rooms', kwargs={'pk':Hoteldelete.pk} )



class DeleteRoomView(AllAdminMixin,DeleteView):
    model = Room
    template_name = 'admin_template/rooms/room_delete.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        rooms_obj = Room.objects.get(id=self.kwargs['pk'])
        roomdelete = Hotel.objects.get(room=rooms_obj)
        context['Hotel'] = roomdelete
        return context

    def get_success_url(self):
        Hotelupdate = Hotel.objects.get(room = self.kwargs['pk'])   
        return reverse_lazy('rooms:admin_rooms', kwargs={'pk':Hotelupdate.pk} )


#room_types view
class RoomTypeCreateView(SuperUserRequiredMixin,CreateView):
    model = RoomType
    form_class = RoomTypeForm
    template_name = 'admin_template/rooms/room_type_create.html'
    success_url = reverse_lazy ('rooms:room_type_list')

class RoomTypeListView(AllAdminMixin,ListView):
    model = RoomType
    template_name = 'admin_template/rooms/room_type_list.html'
    context_object_name = 'room_types'

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

class RoomTypeDetailView(AllAdminMixin,DetailView):
    model = RoomType
    template_name = 'admin_template/rooms/room_type_details.html'
    context_object_name = 'room_types'

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

class RoomTypeUpdateView(SuperUserRequiredMixin,UpdateView):
    model = RoomType
    form_class = RoomTypeForm
    template_name = 'admin_template/rooms/room_type_update.html'
    success_url = reverse_lazy ('rooms:room_type_list')

class RoomTypeDeleteView(SuperUserRequiredMixin,DeleteView):
    model = RoomType
    template_name = 'admin_template/rooms/room_type_delete.html'
    success_url = reverse_lazy ('rooms:room_type_list')




#frontend side roomlist
class RoomViewListView(LoginRequiredMixin,ListView):
    model = Room
    template_name = 'user_templates/room.html'
    context_object_name = 'rooms'


    def get_queryset(self):
        #hotel pk pass
        hotel = self.kwargs['pk']
        #get query set that get me room of only that holte which i clicked on
        queryset = Room.objects.filter(hotel_id=hotel)
        return queryset