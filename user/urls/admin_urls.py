from django.urls import path
from user.views import user_views as views


app_name = 'admin_user'

urlpatterns = [    
    path('user_list',views.HotelUserListView.as_view(),name = 'user_list'),
    path('<int:pk>/details/',views.HotelUserDetailView.as_view(),name = 'user_details'),
    path('<int:pk>/delete/',views.HotelUserDeleteView.as_view(),name = 'user_delete'),
    path('jesondata_User/',views.DataTablesAjaxPagination_User.as_view(),name='jesondata_User'),    
]