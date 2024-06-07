from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ParkingLot, Floor, Slot, Vehicle, Ticket
from .serializers import ParkingLotSerializer, FloorSerializer, SlotSerializer, VehicleSerializer, TicketSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




@swagger_auto_schema(
    method='post',
    request_body=ParkingLotSerializer,
    responses={
        201: ParkingLotSerializer,
        400: 'Bad Request'
    }
)

@api_view(['POST'])
def create_parking_lot(request):
    serializer = ParkingLotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
    method='post',
    request_body=FloorSerializer,
    responses={
        201: FloorSerializer,
        400: 'Bad Request'
    }
)

@api_view(['POST'])
def add_floor(request):
    serializer = FloorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@swagger_auto_schema(
    method='post',
    request_body=SlotSerializer,
    responses={
        201: SlotSerializer,
        400: 'Bad Request'
    }
)
@api_view(['POST'])
def add_slot(request):
    serializer = SlotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'vehicle': openapi.Schema(type=openapi.TYPE_OBJECT)
        },
        required=['vehicle']
    ),
    responses={
        201: TicketSerializer,
        400: 'Bad Request'
    }
)
@api_view(['POST'])
def park_vehicle(request):
    vehicle_data = request.data.get('vehicle')
    vehicle_serializer = VehicleSerializer(data=vehicle_data)
    if vehicle_serializer.is_valid():
        vehicle = vehicle_serializer.save()
        slots = Slot.objects.filter(slot_type=vehicle.type, is_occupied=False).order_by('floor__floor_number', 'slot_number')
        if slots.exists():
            slot = slots.first()
            slot.is_occupied = True
            slot.save()
            ticket_id = f"PR1234_{slot.floor.floor_number}_{slot.slot_number}"
            ticket = Ticket.objects.create(ticket_id=ticket_id, vehicle=vehicle, slot=slot)
            ticket_serializer = TicketSerializer(ticket)
            return Response(ticket_serializer.data, status=status.HTTP_201_CREATED)
        else:
            vehicle.delete()
            return Response({'error': 'No available slots'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(vehicle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ticket_id': openapi.Schema(type=openapi.TYPE_STRING)
        },
        required=['ticket_id']
    ),
    responses={
        200: 'Vehicle unparked successfully',
        400: 'Invalid ticket id'
    }
)
@api_view(['POST'])
def unpark_vehicle(request):
    ticket_id = request.data.get('ticket_id')
    try:
        ticket = Ticket.objects.get(ticket_id=ticket_id, is_active=True)
        ticket.is_active = False
        ticket.save()
        slot = ticket.slot
        slot.is_occupied = False
        slot.save()
        return Response({'message': 'Vehicle unparked successfully'}, status=status.HTTP_200_OK)
    except Ticket.DoesNotExist:
        return Response({'error': 'Invalid ticket id'}, status=status.HTTP_400_BAD_REQUEST)




@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('vehicle_type', openapi.IN_PATH, description="Vehicle type", type=openapi.TYPE_STRING)
    ],
    responses={
        200: 'Success',
        400: 'Bad Request'
    }
)
@api_view(['GET'])
def get_free_slots_count(request, vehicle_type):
    floors = Floor.objects.all()
    data = []
    for floor in floors:
        free_slots = Slot.objects.filter(floor=floor, slot_type=vehicle_type, is_occupied=False).count()
        data.append({'floor': floor.floor_number, 'free_slots': free_slots})
    return Response(data, status=status.HTTP_200_OK)




@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('vehicle_type', openapi.IN_PATH, description="Vehicle type", type=openapi.TYPE_STRING)
    ],
    responses={
        200: 'Success',
        400: 'Bad Request'
    }
)
@api_view(['GET'])
def get_all_free_slots(request, vehicle_type):
    floors = Floor.objects.all()
    data = []
    for floor in floors:
        free_slots = Slot.objects.filter(floor=floor, slot_type=vehicle_type, is_occupied=False)
        slots_data = SlotSerializer(free_slots, many=True).data
        data.append({'floor': floor.floor_number, 'free_slots': slots_data})
    return Response(data, status=status.HTTP_200_OK)




@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('vehicle_type', openapi.IN_PATH, description="Vehicle type", type=openapi.TYPE_STRING)
    ],
    responses={
        200: 'Success',
        400: 'Bad Request'
    }
)
@api_view(['GET'])
def get_all_occupied_slots(request, vehicle_type):
    floors = Floor.objects.all()
    data = []
    for floor in floors:
        occupied_slots = Slot.objects.filter(floor=floor, slot_type=vehicle_type, is_occupied=True)
        slots_data = SlotSerializer(occupied_slots, many=True).data
        data.append({'floor': floor.floor_number, 'occupied_slots': slots_data})
    return Response(data, status=status.HTTP_200_OK)
