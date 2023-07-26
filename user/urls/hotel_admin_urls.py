from django.urls import path
from user.views import admin_views as views

app_name = 'hotel_admins'

urlpatterns = [

#hotel_admin
    path('hoteladmin_list/', views.HotelAdminListView.as_view(), name='hoteladmin_list'),
    path('hoteladmin_create/', views.HotelAdminCreateView.as_view(), name='hoteladmin_create'),
    path('<int:pk>/detail/', views.HotelAdminDetailView.as_view(), name='hoteladmin_detail'),
    path('<int:pk>/update/', views.HotelAdminUpdateView.as_view(), name='hoteladmin_update'),
    path('<int:pk>/delete/', views.HotelAdminDeleteView.as_view(), name='hoteladmin_delete'),
    path('jesondata_HotelAdmin/',views.DataTablesAjaxPagination_HotelAdmin.as_view(),name='jesondata_HotelAdmin'),

]






























  # path('deshboard/',views.HomePageDispatchView.as_view(),name = 'deshboard')    