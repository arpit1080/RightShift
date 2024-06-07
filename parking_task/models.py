from django.db import models

class ParkingLot(models.Model):
    parking_lot_id = models.CharField(max_length=10, default='PR1234')

class Floor(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    floor_number = models.IntegerField()

class Slot(models.Model):
    SLOT_TYPE_CHOICES = [
        ('Car', 'Car'),
        ('Bike', 'Bike'),
        ('Truck', 'Truck'),
    ]
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    slot_number = models.IntegerField()
    slot_type = models.CharField(max_length=5, choices=SLOT_TYPE_CHOICES)
    is_occupied = models.BooleanField(default=False)

class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('Car', 'Car'),
        ('Bike', 'Bike'),
        ('Truck', 'Truck'),
    ]
    type = models.CharField(max_length=5, choices=VEHICLE_TYPE_CHOICES)
    registration_number = models.CharField(max_length=15)
    color = models.CharField(max_length=20)

class Ticket(models.Model):
    ticket_id = models.CharField(max_length=20)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
