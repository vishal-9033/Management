from django.urls import path
from rooms.views import rooms_view as views

app_name='rooms'

urlpatterns = [

    #urls for roomtypes
   
    path('room_type_create/', views.RoomTypeCreateView.as_view(), name='room_type_create'),
    path('room_type_list/', views.RoomTypeListView.as_view(), name='room_type_list'),
    path('<int:pk>/room_type_detail/', views.RoomTypeDetailView.as_view(), name='room_type_detail'),
    path('<int:pk>/room_type_update/', views.RoomTypeUpdateView.as_view(), name='room_type_update'),
    path('<int:pk>/room_type_delete/', views.RoomTypeDeleteView.as_view(), name='room_type_delete'),




    #urls for rooms
    path('<int:pk>/admin_rooms/', views.RoomListView.as_view(), name='admin_rooms'),
    path('<int:pk>/details/', views.RooomDetailView.as_view(), name='details_rooms'),
    path('<int:pk>/add_rooms', views.AddRoomView.as_view(), name='add_rooms'),
    path('<int:pk>/update/', views.UpdateRoomView.as_view(), name='update_rooms'),
    path('<int:pk>/delete/', views.DeleteRoomView.as_view(),name='delete_rooms'),
    path('<int:pk>/jesondata_room/', views.DataTablesAjaxPaginationRooms.as_view(),name='jesondata_room'),


    #urls for userview
    path('<int:pk>/all_rooms/',views.RoomViewListView.as_view(),name='all_rooms'),
    
]
