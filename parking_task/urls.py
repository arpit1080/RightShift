from django.urls import path
from .views import create_parking_lot,add_floor,add_slot,park_vehicle,unpark_vehicle,get_free_slots_count,get_all_occupied_slots,get_all_free_slots

urlpatterns = [
    path('create_parking_lot/', create_parking_lot, name='create_parking_lot'),
    path('add_floor/', add_floor, name='add_floor'),
    path('add_slot/', add_slot, name='add_slot'),
    path('park_vehicle/', park_vehicle, name='park_vehicle'),
    path('unpark_vehicle/', unpark_vehicle, name='unpark_vehicle'),
    path('free_slots_count/<str:vehicle_type>/', get_free_slots_count, name='free_slots_count'),
    path('all_free_slots/<str:vehicle_type>/', get_all_free_slots, name='all_free_slots'),
    path('all_occupied_slots/<str:vehicle_type>/', get_all_occupied_slots, name='all_occupied_slots'),
]
