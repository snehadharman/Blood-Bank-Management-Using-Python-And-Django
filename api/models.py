from django.db import models


class Donor(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]

    name = models.CharField(max_length=255)
    age = models.IntegerField()
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.blood_type})"



class BloodInventory(models.Model):
    blood_type = models.CharField(max_length=3, unique=True)
    units = models.IntegerField(default=0)

class BloodRequest(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3)
    units_requested = models.IntegerField()
    status = models.CharField(max_length=10, choices=[
        ('Pending', 'Pending'),
        ('Fulfilled', 'Fulfilled'),
    ], default='Pending')