from rest_framework import serializers
from .models import ParkingLot, Floor, Slot, Vehicle, Ticket

class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        fields = ["parking_lot_id"]

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['parking_lot','floor_number']

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['is_occupied','slot_type','slot_number','floor']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['color','registration_number','type']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['ticket_id','issued_at','is_active','slot','vehicle']

