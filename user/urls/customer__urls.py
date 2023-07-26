from django.urls import path
from user.views import user_views as views
# from accounts.views import  *
app_name = 'user'

urlpatterns = [
    #hotel_static
    path('accounts/signup/',views.HotelUserCreateView.as_view(),name = 'signup'),
    path('',views.main_index.as_view(),name='index'),
    path('about/',views.main_about.as_view(),name='about'),
    path('service/',views.main_service.as_view(),name='service'),
    path('contact/',views.main_contact.as_view(),name='contact'),
    path('<int:pk>/profile/',views.UserProfileView.as_view(),name='profile'),
    path('<int:pk>/update_profile/',views.UserUpdateView.as_view(),name='update_profile'),
    path('<int:pk>/delete_profile/',views.UserDeleteView.as_view(),name='delete_profile'),
    
    
]