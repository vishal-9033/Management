from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from allauth.account.forms import SignupForm
from allauth.account.views import SignupView
from user.custom_form import *
from user.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView,RedirectView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from hotels.models import *
from rooms.models import *
from base.mixin import *
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import View
from django_datatables_too.mixins import DataTableMixin



#static_templates
class main_index(TemplateView):
    template_name = 'user_templates/index.html'

class main_about(TemplateView):
    template_name ='user_templates/about.html'

class main_service(TemplateView):
    template_name ='user_templates/service.html'

class main_contact(TemplateView):
    template_name ='user_templates/contact.html'


#customer list admin side
class HotelUserListView(SuperUserRequiredMixin,ListView):
    model = HotelUser
    template_name = 'admin_template/user/user_list.html'
    context_object_name = 'users'
    queryset = HotelUser.objects.none()

       
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)     
        context['Hotel'] = Hotel.objects.all()
        return context


class DataTablesAjaxPagination_User(DataTableMixin, View):
    
    def get_queryset(self):
        queryset = HotelUser.objects.filter(user_type=3)
        return queryset
    

    def _get_actions(self, obj):
        """Get action buttons w/links."""
        return f'<a data-title="{obj}" title="detail" href="{obj.get_detailuser_url()}" class="btn btn-info"><i class="bi bi-info-lg"></i></a> <a data-title="{obj}" title="Delete" href="{obj.get_deleteuser_url()}" class="btn btn-danger btn-xs btn-delete"><i class="bi bi-trash-fill"></i></a>'

    def filter_queryset(self, qs):
        if self.search:
            return qs.filter(                
                # Q(user__id__icontains=self.search) |
                Q(username__icontains=self.search) |
                Q(email__icontains=self.search) |
                Q(city__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append({                
                # 'user.id': o.pk,
                'username': o.username,
                'email': o.email,
                'city':o.city,
                'actions': self._get_actions(o)        
            })      
        return data

    def get(self, request):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)



#customer_details(admin side)
class HotelUserDetailView(SuperUserRequiredMixin,DetailView):
    model = HotelUser
    template_name = 'admin_template/user/user_detail.html'
    context_object_name = 'users'


class HotelUserDeleteView(SuperUserRequiredMixin,DeleteView):
    model = HotelUser
    template_name = 'admin_template/user/user_delete.html'
    success_url = reverse_lazy ('admin_user:user_list')


#customer_customer side
class HotelUserCreateView(SignupView):
    model = HotelUser
    form_class = CustomSignupForm
    template_name = 'user_templates/signup.html'


class UserProfileView(LoginRequiredMixin,DetailView):
    model = HotelUser
    template_name = 'user_templates/profile.html'
    context_object_name = 'users'



class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = HotelUser
    form_class = UpdateUserForm
    template_name = 'user_templates/updateprofile.html'
    

    def get_success_url(self):
        return reverse_lazy('user:profile',kwargs={'pk':self.kwargs['pk']})

    
class UserDeleteView(LoginRequiredMixin,DeleteView):
    model = HotelUser
    template_name = 'user_templates/deleteprofile.html'
    success_url = reverse_lazy ('user:index')