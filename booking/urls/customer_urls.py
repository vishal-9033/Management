from django.urls import path
from booking.views import booking_views as views


app_name = 'booking' 

urlpatterns = [

    # #urls for customer side roombooking(check,booking,list,details,cancel)
    path('<int:pk>/CreateBooking', views.CheckRoomCreateView.as_view(), name='CreateBooking'),
    path('<int:pk>/GuestForm',views.GuestFormCreateView.as_view(),name='GuestForm'),
    path('<int:pk>/BookingList',views.BookingListView.as_view(),name='BookingList'),
    # path('<int:pk>/BookingDetails/',views.BookingDetailsView.as_view(),name='BookingDetails'),
    path('<int:pk>/BookingCancel/',views.BookingCancelDeleteView.as_view(),name='BookingCancel'),

    # #urls for admin side roombooking(list,details,cancel)
    path('<int:pk>/listofbooking/',views.ListOfBookingViewListView.as_view(),name='listofbooking'),
    path('<int:pk>/detailofbooking/',views.DetailsOfBookingViewDetailView.as_view(),name='detailofbooking'),
    # path('<int:pk>/CancelBooking/',views.CancelBookingDeleteView.as_view(),name='cancelbooking'),
]
