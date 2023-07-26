from django.urls import path
from hotels.views import hotels_view as views
app_name = 'hotels'

urlpatterns = [

    #admin_side_hotelurls
    path('all',views.HotelListView.as_view(),name='all'),
    path('add',views.AddHotelView.as_view(),name='add'),
    path('<int:pk>/update/',views.UpdateHotelView.as_view(),name='update'),
    path('<int:pk>/delete/',views.DeleteHotelView.as_view(),name='delete'),
    path('<int:pk>/details/',views.HotelDetailView.as_view(),name='details'),
    path('jesondata_hotel/',views.DataTablesAjaxPagination.as_view(),name='jesondata_hotel'),


    #user_side_hotelurls
    path('all_hotels/',views.HotelViewListView.as_view(),name='all_hotels'),

]




























    # path('reservation/<int:pk>/',views.ReservationCreateView.as_view(),name='reservation'),
    # path('reservation/<int:pk>/confirm/',views.ReservationConfirmView.as_view(),name='confirm'),
    # path('reservation/<int:pk>/cancel/',views.ReservationCancelView.as_view(),name='cancel'),